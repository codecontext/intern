from pathlib import Path
from uuid import uuid4

import pytest

from intern.chunking.models import DocumentChunk
from intern.embeddings.base import EmbeddingProvider
from intern.embeddings.ollama import OllamaEmbeddingProvider
from intern.embeddings.service import EmbeddingError, EmbeddingService


def make_chunk(content: str, index: int) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=uuid4(),
        document_id=uuid4(),
        source_path=Path("/workspace/notes.md"),
        relative_path=Path("notes.md"),
        chunk_index=index,
        start_offset=index * 5,
        end_offset=index * 5 + len(content),
        content=content,
    )


class FakeEmbeddingProvider(EmbeddingProvider):
    def __init__(self, vectors: list[list[float]]):
        self.vectors = vectors
        self.calls: list[tuple[str, list[str]]] = []

    def embed(self, model: str, texts: list[str]) -> list[list[float]]:
        self.calls.append((model, texts))
        return self.vectors


def test_embedding_service_preserves_chunk_order_and_provenance() -> None:
    chunks = [make_chunk("first", 0), make_chunk("second", 1)]
    provider = FakeEmbeddingProvider([[1.0, 2.0], [3.0, 4.0]])

    embedded = EmbeddingService(provider).embed_chunks("local-model", chunks)

    assert provider.calls == [("local-model", ["first", "second"])]
    assert [item.chunk for item in embedded] == chunks
    assert [item.embedding for item in embedded] == [
        (1.0, 2.0),
        (3.0, 4.0),
    ]


def test_empty_chunks_do_not_call_provider() -> None:
    provider = FakeEmbeddingProvider([])

    assert EmbeddingService(provider).embed_chunks("local-model", []) == []
    assert provider.calls == []


@pytest.mark.parametrize("model", ["", "   "])
def test_empty_model_raises_error(model: str) -> None:
    with pytest.raises(EmbeddingError, match="must not be empty"):
        EmbeddingService(FakeEmbeddingProvider([])).embed_chunks(model, [])


def test_provider_vector_count_must_match_chunk_count() -> None:
    provider = FakeEmbeddingProvider([[1.0]])
    chunks = [make_chunk("first", 0), make_chunk("second", 1)]

    with pytest.raises(EmbeddingError, match="different number"):
        EmbeddingService(provider).embed_chunks("local-model", chunks)


def test_ollama_provider_adapts_embed_response(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeResponse:
        embeddings = [[0.1, 0.2], [0.3, 0.4]]

    captured: dict[str, object] = {}

    def fake_embed(*, model: str, input: list[str]) -> FakeResponse:
        captured["model"] = model
        captured["input"] = input
        return FakeResponse()

    monkeypatch.setattr("intern.embeddings.ollama.ollama.embed", fake_embed)

    vectors = OllamaEmbeddingProvider().embed(
        "nomic-embed-text",
        ("first", "second"),
    )

    assert captured == {
        "model": "nomic-embed-text",
        "input": ["first", "second"],
    }
    assert vectors == [[0.1, 0.2], [0.3, 0.4]]
