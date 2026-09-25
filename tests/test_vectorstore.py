from pathlib import Path
from uuid import uuid4

import pytest

from intern.chunking.models import DocumentChunk
from intern.embeddings.models import EmbeddedChunk
from intern.vectorstore.in_memory import InMemoryVectorStore, VectorStoreError


def make_embedded_chunk(
    content: str,
    vector: tuple[float, ...],
    chunk_id=None,
) -> EmbeddedChunk:
    chunk = DocumentChunk(
        chunk_id=chunk_id or uuid4(),
        document_id=uuid4(),
        source_path=Path("/workspace/notes.md"),
        relative_path=Path("notes.md"),
        chunk_index=0,
        start_offset=0,
        end_offset=len(content),
        content=content,
    )
    return EmbeddedChunk(chunk=chunk, embedding=vector)


def test_upsert_and_search_return_ranked_provenance() -> None:
    store = InMemoryVectorStore()
    close = make_embedded_chunk("close", (1.0, 0.0))
    far = make_embedded_chunk("far", (0.0, 1.0))
    store.upsert([far, close])

    results = store.search((0.9, 0.1), top_k=2)

    assert store.count() == 2
    assert [result.chunk_id for result in results] == [
        close.chunk.chunk_id,
        far.chunk.chunk_id,
    ]
    assert results[0].chunk.content == "close"
    assert results[0].score > results[1].score


def test_top_k_limits_results() -> None:
    store = InMemoryVectorStore()
    store.upsert(
        [
            make_embedded_chunk("one", (1.0, 0.0)),
            make_embedded_chunk("two", (0.8, 0.2)),
        ]
    )

    assert len(store.search((1.0, 0.0), top_k=1)) == 1


def test_upsert_replaces_existing_chunk() -> None:
    store = InMemoryVectorStore()
    chunk_id = uuid4()
    original = make_embedded_chunk("original", (1.0, 0.0), chunk_id)
    replacement = make_embedded_chunk("replacement", (0.0, 1.0), chunk_id)

    store.upsert([original])
    store.upsert([replacement])

    assert store.count() == 1
    assert store.search((0.0, 1.0))[0].chunk.content == "replacement"


def test_zero_norm_vectors_have_zero_similarity() -> None:
    store = InMemoryVectorStore()
    store.upsert([make_embedded_chunk("zero", (0.0, 0.0))])

    assert store.search((1.0, 0.0))[0].score == 0.0


@pytest.mark.parametrize(
    ("query", "top_k", "message"),
    [
        ((), 5, "Query embedding must not be empty"),
        ((1.0,), 0, "top_k must be greater than zero"),
    ],
)
def test_invalid_search_input_raises_error(
    query: tuple[float, ...],
    top_k: int,
    message: str,
) -> None:
    with pytest.raises(VectorStoreError, match=message):
        InMemoryVectorStore().search(query, top_k)


def test_empty_stored_embedding_raises_error() -> None:
    with pytest.raises(VectorStoreError, match="must not be empty"):
        InMemoryVectorStore().upsert([make_embedded_chunk("empty", ())])


def test_embedding_dimensions_must_match() -> None:
    store = InMemoryVectorStore()
    store.upsert([make_embedded_chunk("stored", (1.0, 0.0))])

    with pytest.raises(VectorStoreError, match="dimensions must match"):
        store.search((1.0,))
