from pathlib import Path
from uuid import UUID

from fastapi.testclient import TestClient

from intern.api.app import create_app
from intern.application.chat import ChatService
from intern.knowledge_base.service import KnowledgeBaseService
from intern.llm.base import LLM


class FakeLLM(LLM):
    def list_models(self) -> list[str]:
        return ["fake-model"]

    def chat(self, model: str, messages: list[dict[str, str]]) -> str:
        return "response"


def test_knowledge_base_service_ingests_and_retrieves(tmp_path: Path) -> None:
    (tmp_path / "notes.md").write_text("hello", encoding="utf-8")

    service = KnowledgeBaseService()
    knowledge_base = service.create([tmp_path])

    assert knowledge_base.source_paths == (tmp_path.resolve(),)
    assert len(knowledge_base.documents) == 1
    assert service.get(knowledge_base.knowledge_base_id) == knowledge_base
    assert service.list() == [knowledge_base]


def test_adding_a_source_replaces_the_active_snapshot(tmp_path: Path) -> None:
    first_path = tmp_path / "first.md"
    second_path = tmp_path / "second.md"
    first_path.write_text("first", encoding="utf-8")
    second_path.write_text("second", encoding="utf-8")
    service = KnowledgeBaseService()

    service.create([first_path])
    active = service.create([first_path, second_path])

    assert service.list() == [active]
    assert active.source_paths == (first_path.resolve(), second_path.resolve())
    assert len(active.documents) == 2


def test_knowledge_base_api_lists_and_creates(tmp_path: Path) -> None:
    application = create_app(
        configured_chat_service=ChatService(FakeLLM()),
    )
    client = TestClient(application)
    (tmp_path / "notes.txt").write_text("hello", encoding="utf-8")

    create_response = client.post(
        "/api/knowledge-bases",
        json={"source_paths": [str(tmp_path)]},
    )

    assert create_response.status_code == 201
    data = create_response.json()
    assert data["source_paths"] == [str(tmp_path.resolve())]
    assert data["document_count"] == 1
    assert UUID(data["knowledge_base_id"])

    list_response = client.get("/api/knowledge-bases")
    assert list_response.status_code == 200
    assert list_response.json() == [data]


def test_knowledge_base_api_rejects_invalid_directory(tmp_path: Path) -> None:
    application = create_app(
        configured_chat_service=ChatService(FakeLLM()),
    )
    client = TestClient(application)

    response = client.post(
        "/api/knowledge-bases",
        json={"source_paths": [str(tmp_path / "missing")]},
    )

    assert response.status_code == 400
    assert "does not exist" in response.json()["detail"]


def test_knowledge_base_api_validates_paths_before_loading(
    tmp_path: Path,
) -> None:
    application = create_app(
        configured_chat_service=ChatService(FakeLLM()),
    )
    client = TestClient(application)
    valid_path = tmp_path / "notes.md"
    valid_path.write_text("hello", encoding="utf-8")

    valid_response = client.post(
        "/api/knowledge-bases/validate",
        json={"source_paths": [str(valid_path)]},
    )
    invalid_response = client.post(
        "/api/knowledge-bases/validate",
        json={"source_paths": [str(tmp_path / "missing.txt")]},
    )

    assert valid_response.status_code == 200
    assert valid_response.json() == {"valid": True}
    assert invalid_response.status_code == 400
    assert "does not exist" in invalid_response.json()["detail"]


def test_knowledge_base_api_rejects_empty_path() -> None:
    application = create_app(
        configured_chat_service=ChatService(FakeLLM()),
    )
    client = TestClient(application)

    response = client.post(
        "/api/knowledge-bases",
        json={"source_paths": ["   "]},
    )

    assert response.status_code == 422
