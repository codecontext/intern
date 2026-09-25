from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

from intern.application.chat import ChatService
from intern.application.repository import ConversationRepository


class ConversationNotFoundError(LookupError):
    """Raised when a conversation ID is not present in the repository."""


@dataclass(frozen=True)
class Message:
    role: Literal["user", "assistant"]
    content: str


@dataclass
class Conversation:
    conversation_id: UUID
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ConversationService:
    """Orchestrate conversation state and assistant response generation."""

    def __init__(
        self,
        repository: ConversationRepository,
        chat_service: ChatService,
    ):
        self._repository = repository
        self._chat_service = chat_service

    def create_conversation(self) -> Conversation:
        conversation = Conversation(conversation_id=uuid4())
        self._repository.create(conversation)
        return conversation

    def get_conversation(self, conversation_id: UUID) -> Conversation:
        conversation = self._repository.get(conversation_id)

        if conversation is None:
            raise ConversationNotFoundError(str(conversation_id))

        return conversation

    def add_message(
        self,
        conversation_id: UUID,
        message: Message,
    ) -> Conversation:
        conversation = self.get_conversation(conversation_id)
        conversation.messages.append(message)
        conversation.updated_at = datetime.now(timezone.utc)
        self._repository.update(conversation)
        return conversation

    def get_messages(self, conversation_id: UUID) -> list[Message]:
        return list(self.get_conversation(conversation_id).messages)

    def add_user_message_and_respond(
        self,
        conversation_id: UUID,
        model: str,
        content: str,
    ) -> str:
        self.add_message(
            conversation_id,
            Message(role="user", content=content),
        )
        response = self._chat_service.chat(
            model=model,
            messages=[
                {"role": message.role, "content": message.content}
                for message in self.get_messages(conversation_id)
            ],
        )
        self.add_message(
            conversation_id,
            Message(role="assistant", content=response),
        )
        return response
