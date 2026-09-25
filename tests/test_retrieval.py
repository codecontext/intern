from pathlib import Path
from uuid import uuid4

import pytest

from intern.chunking.models import DocumentChunk
from intern.embeddings.base import EmbeddingProvider
from intern.embeddings.models import EmbeddedChunk
from intern.embeddings.service import EmbeddingService
from intern.retrieval.service import RetrievalError, RetrievalService
from intern.vectorstore.in_memory import InMemoryVectorStore


class FakeEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.calls: list[tuple[str, list[str]]] = []

    def embed(self, model: str, texts: list[str]) -> list[list[float]]:
        self.calls.append((model, texts))
        return [[1.0, 0.0] for _ in texts]


def make_chunk(content: str, index: int) -> DocumentChunk:
    return DocumentChunk(
        chunk_id=uuid4(),
        document_id=uuid4(),
        source_path=Path("/workspace/docs/notes.md"),
        relative_path=Path("docs/notes.md"),
        chunk_index=index,
        start_offset=index * 10,
        end_offset=index * 10 + len(content),
        content=content,
    )


def test_retrieve_embeds_query_and_returns_ranked_chunks() -> None:
    provider = FakeEmbeddingProvider()
    embedding_service = EmbeddingService(provider)
    vector_store = InMemoryVectorStore()
    first = make_chunk("first", 0)
    second = make_chunk("second", 1)
    vector_store.upsert(
        [
            EmbeddedChunk(first, (1.0, 0.0)),
            EmbeddedChunk(second, (0.0, 1.0)),
        ]
    )

    results = RetrievalService(
        embedding_service,
        vector_store,
    ).retrieve(
        query="what is relevant?",
        embedding_model="fake-embedding-model",
        top_k=1,
    )

    assert provider.calls == [("fake-embedding-model", ["what is relevant?"])]
    assert len(results) == 1
    assert results[0].chunk_id == first.chunk_id
    assert results[0].chunk.content == "first"


def test_retrieve_empty_store_returns_no_results() -> None:
    service = RetrievalService(
        EmbeddingService(FakeEmbeddingProvider()),
        InMemoryVectorStore(),
    )

    assert service.retrieve("query", "fake-model") == []


@pytest.mark.parametrize(
    ("query", "top_k", "message"),
    [
        ("   ", 5, "Query must not be empty"),
        ("query", 0, "top_k must be greater than zero"),
    ],
)
def test_invalid_retrieval_request_raises_error(
    query: str,
    top_k: int,
    message: str,
) -> None:
    service = RetrievalService(
        EmbeddingService(FakeEmbeddingProvider()),
        InMemoryVectorStore(),
    )

    with pytest.raises(RetrievalError, match=message):
        service.retrieve(query, "fake-model", top_k)


def test_empty_embedding_model_is_rejected() -> None:
    service = RetrievalService(
        EmbeddingService(FakeEmbeddingProvider()),
        InMemoryVectorStore(),
    )

    with pytest.raises(RetrievalError):
        service.retrieve("query", "   ")


def test_context_assembly_preserves_source_and_order() -> None:
    first = make_chunk("first content", 0)
    second = make_chunk("second content", 1)
    vector_store = InMemoryVectorStore()
    vector_store.upsert(
        [
            EmbeddedChunk(first, (1.0, 0.0)),
            EmbeddedChunk(second, (0.9, 0.1)),
        ]
    )
    service = RetrievalService(
        EmbeddingService(FakeEmbeddingProvider()),
        vector_store,
    )

    results = service.retrieve("query", "fake-model", top_k=2)

    assert service.assemble_context(results) == (
        "[Source: docs/notes.md]\nfirst content\n\n"
        "[Source: docs/notes.md]\nsecond content"
    )
