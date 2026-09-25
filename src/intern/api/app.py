from datetime import datetime
from pathlib import Path
from typing import Literal
from uuid import UUID

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from intern.application.chat import ChatService
from intern.application.conversation import (
    Conversation,
    ConversationNotFoundError,
    ConversationService,
)
from intern.application.repository import InMemoryConversationRepository
from intern.ingestion.service import IngestionError
from intern.knowledge_base.models import KnowledgeBase
from intern.knowledge_base.service import KnowledgeBaseService
from intern.llm.ollama import OllamaLLM

WEB_DIR = Path(__file__).resolve().parents[1] / "web"


class ConversationCreatedResponse(BaseModel):
    conversation_id: UUID


class MessageResponse(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ConversationResponse(BaseModel):
    conversation_id: UUID
    messages: list[MessageResponse]
    created_at: datetime
    updated_at: datetime


class AddMessageRequest(BaseModel):
    model: str = Field(min_length=1)
    message: str = Field(min_length=1)

    @field_validator("model", "message")
    @classmethod
    def reject_whitespace_only(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("must not be empty")

        return value


class AssistantResponse(BaseModel):
    response: str


class KnowledgeBaseCreateRequest(BaseModel):
    source_paths: list[str] = Field(min_length=1)

    @field_validator("source_paths")
    @classmethod
    def reject_empty_paths(cls, value: list[str]) -> list[str]:
        paths = [path.strip() for path in value]

        if not paths or any(not path for path in paths):
            raise ValueError("source paths must not be empty")

        return paths


class KnowledgeBaseResponse(BaseModel):
    knowledge_base_id: UUID
    source_paths: list[str]
    document_count: int
    created_at: datetime


class KnowledgeBaseValidationResponse(BaseModel):
    valid: bool


def serialize_knowledge_base(
    knowledge_base: KnowledgeBase,
) -> KnowledgeBaseResponse:
    return KnowledgeBaseResponse(
        knowledge_base_id=knowledge_base.knowledge_base_id,
        source_paths=[str(path) for path in knowledge_base.source_paths],
        document_count=len(knowledge_base.documents),
        created_at=knowledge_base.created_at,
    )


def serialize_conversation(conversation: Conversation) -> ConversationResponse:
    return ConversationResponse(
        conversation_id=conversation.conversation_id,
        messages=[
            MessageResponse(role=message.role, content=message.content)
            for message in conversation.messages
        ],
        created_at=conversation.created_at.isoformat(),
        updated_at=conversation.updated_at.isoformat(),
    )


def create_app(
    configured_chat_service: ChatService | None = None,
    configured_conversation_service: ConversationService | None = None,
    configured_knowledge_base_service: KnowledgeBaseService | None = None,
) -> FastAPI:
    application = FastAPI(
        title="Intern",
        description="Context-aware knowledge assistant",
        version="0.1.0",
    )

    application.mount(
        "/static",
        StaticFiles(directory=WEB_DIR),
        name="static",
    )

    app_chat_service = configured_chat_service or ChatService(llm=OllamaLLM())
    app_conversation_service = (
        configured_conversation_service
        or ConversationService(
            InMemoryConversationRepository(),
            app_chat_service,
        )
    )
    app_knowledge_base_service = (
        configured_knowledge_base_service or KnowledgeBaseService()
    )

    @application.get("/")
    def index() -> FileResponse:
        return FileResponse(WEB_DIR / "index.html")

    @application.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.get("/api/models")
    def models() -> list[str]:
        return app_chat_service.list_models()

    @application.get(
        "/api/knowledge-bases",
        response_model=list[KnowledgeBaseResponse],
    )
    def list_knowledge_bases() -> list[KnowledgeBaseResponse]:
        return [
            serialize_knowledge_base(knowledge_base)
            for knowledge_base in app_knowledge_base_service.list()
        ]

    @application.post(
        "/api/knowledge-bases/validate",
        response_model=KnowledgeBaseValidationResponse,
    )
    def validate_knowledge_base_paths(
        request: KnowledgeBaseCreateRequest,
    ) -> KnowledgeBaseValidationResponse:
        try:
            app_knowledge_base_service.validate_paths(
                [Path(path) for path in request.source_paths],
            )
        except (IngestionError, ValueError) as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

        return KnowledgeBaseValidationResponse(valid=True)

    @application.post(
        "/api/knowledge-bases",
        response_model=KnowledgeBaseResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_knowledge_base(
        request: KnowledgeBaseCreateRequest,
    ) -> KnowledgeBaseResponse:
        try:
            knowledge_base = app_knowledge_base_service.create(
                [Path(path) for path in request.source_paths],
            )
        except IngestionError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

        return serialize_knowledge_base(knowledge_base)

    @application.post(
        "/api/conversations",
        response_model=ConversationCreatedResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_conversation() -> ConversationCreatedResponse:
        conversation = app_conversation_service.create_conversation()
        return ConversationCreatedResponse(
            conversation_id=conversation.conversation_id,
        )

    @application.get(
        "/api/conversations/{conversation_id}",
        response_model=ConversationResponse,
    )
    def get_conversation(conversation_id: UUID) -> ConversationResponse:
        try:
            conversation = app_conversation_service.get_conversation(
                conversation_id,
            )
        except ConversationNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            ) from error

        return serialize_conversation(conversation)

    @application.post(
        "/api/conversations/{conversation_id}/messages",
        response_model=AssistantResponse,
    )
    def add_message(
        conversation_id: UUID,
        request: AddMessageRequest,
    ) -> AssistantResponse:
        try:
            response = app_conversation_service.add_user_message_and_respond(
                conversation_id=conversation_id,
                model=request.model,
                content=request.message,
            )
        except ConversationNotFoundError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found",
            ) from error
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="The language model failed to generate a response",
            ) from error

        return AssistantResponse(response=response)

    return application


app = create_app()
