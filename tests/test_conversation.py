from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from intern.api.app import create_app
from intern.application.chat import ChatService
from intern.application.conversation import (
    ConversationNotFoundError,
    ConversationService,
    Message,
)
from intern.application.repository import InMemoryConversationRepository
from intern.llm.base import LLM


class FakeLLM(LLM):
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail
        self.calls: list[tuple[str, list[dict[str, str]]]] = []

    def list_models(self) -> list[str]:
        return ["fake-model"]

    def chat(self, model: str, messages: list[dict[str, str]]) -> str:
        if self.should_fail:
            raise RuntimeError("fake provider failure")

        self.calls.append((model, messages))
        return f"reply to: {messages[-1]['content']}"


@pytest.fixture
def conversation_service() -> ConversationService:
    return ConversationService(
        InMemoryConversationRepository(),
        ChatService(FakeLLM()),
    )


def test_creating_and_retrieving_conversation(
    conversation_service: ConversationService,
) -> None:
    conversation = conversation_service.create_conversation()

    retrieved = conversation_service.get_conversation(
        conversation.conversation_id,
    )

    assert retrieved.conversation_id == conversation.conversation_id
    assert retrieved.messages == []
    assert retrieved.created_at == conversation.created_at
    assert retrieved.updated_at == conversation.updated_at


def test_adding_messages_preserves_order(
    conversation_service: ConversationService,
) -> None:
    conversation = conversation_service.create_conversation()
    conversation_id = conversation.conversation_id

    conversation_service.add_message(
        conversation_id,
        Message(role="user", content="first"),
    )
    conversation_service.add_message(
        conversation_id,
        Message(role="assistant", content="second"),
    )

    assert conversation_service.get_messages(conversation_id) == [
        Message(role="user", content="first"),
        Message(role="assistant", content="second"),
    ]


def test_service_generates_and_stores_assistant_response(
    conversation_service: ConversationService,
) -> None:
    conversation = conversation_service.create_conversation()

    response = conversation_service.add_user_message_and_respond(
        conversation.conversation_id,
        model="fake-model",
        content="hello",
    )

    assert response == "reply to: hello"
    assert conversation_service.get_messages(conversation.conversation_id) == [
        Message(role="user", content="hello"),
        Message(role="assistant", content="reply to: hello"),
    ]


def test_retrieving_nonexistent_conversation(
    conversation_service: ConversationService,
) -> None:
    with pytest.raises(ConversationNotFoundError):
        conversation_service.get_conversation(uuid4())


def test_api_chat_flow_uses_backend_history() -> None:
    fake_llm = FakeLLM()
    application = create_app(
        configured_chat_service=ChatService(fake_llm),
    )
    client = TestClient(application)

    create_response = client.post("/api/conversations")
    conversation_id = create_response.json()["conversation_id"]

    first_response = client.post(
        f"/api/conversations/{conversation_id}/messages",
        json={"model": "fake-model", "message": "first"},
    )
    second_response = client.post(
        f"/api/conversations/{conversation_id}/messages",
        json={"model": "fake-model", "message": "second"},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert fake_llm.calls[1][1] == [
        {"role": "user", "content": "first"},
        {"role": "assistant", "content": "reply to: first"},
        {"role": "user", "content": "second"},
    ]

    conversation_response = client.get(
        f"/api/conversations/{conversation_id}",
    )
    assert [
        message["content"]
        for message in conversation_response.json()["messages"]
    ] == [
        "first",
        "reply to: first",
        "second",
        "reply to: second",
    ]


def test_api_errors_do_not_require_ollama() -> None:
    application = create_app(
        configured_chat_service=ChatService(FakeLLM(should_fail=True)),
    )
    client = TestClient(application)

    missing_response = client.post(
        f"/api/conversations/{uuid4()}/messages",
        json={"model": "fake-model", "message": "hello"},
    )
    assert missing_response.status_code == 404
    assert missing_response.json()["detail"] == "Conversation not found"

    create_response = client.post("/api/conversations")
    conversation_id = UUID(create_response.json()["conversation_id"])

    empty_response = client.post(
        f"/api/conversations/{conversation_id}/messages",
        json={"model": "fake-model", "message": "   "},
    )
    assert empty_response.status_code == 422

    failed_response = client.post(
        f"/api/conversations/{conversation_id}/messages",
        json={"model": "fake-model", "message": "hello"},
    )
    assert failed_response.status_code == 502
    assert "failed to generate" in failed_response.json()["detail"]
