from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from intern.application.conversation import Conversation


class ConversationRepository(ABC):
    """Storage contract for conversation state."""

    @abstractmethod
    def create(self, conversation: Conversation) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, conversation_id: UUID) -> Conversation | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, conversation: Conversation) -> None:
        raise NotImplementedError


class InMemoryConversationRepository(ConversationRepository):
    """Store conversations in process memory for the current application run."""

    def __init__(self):
        self._conversations: dict[UUID, Conversation] = {}

    def create(self, conversation: Conversation) -> None:
        self._conversations[conversation.conversation_id] = conversation

    def get(self, conversation_id: UUID) -> Conversation | None:
        return self._conversations.get(conversation_id)

    def update(self, conversation: Conversation) -> None:
        self._conversations[conversation.conversation_id] = conversation