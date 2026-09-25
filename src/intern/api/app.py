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

    @application.get("/")
    def index() -> FileResponse:
        return FileResponse(WEB_DIR / "index.html")

    @application.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.get("/api/models")
    def models() -> list[str]:
        return app_chat_service.list_models()

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
