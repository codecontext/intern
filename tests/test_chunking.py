from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pytest

from intern.chunking.service import ChunkingError, DocumentChunkingService
from intern.ingestion.models import Document


def make_document(content: str) -> Document:
    return Document(
        document_id=uuid4(),
        source_path=Path("/workspace/notes.md"),
        relative_path=Path("notes.md"),
        filename="notes.md",
        extension=".md",
        content=content,
        size_bytes=len(content.encode("utf-8")),
        modified_at=datetime.now(timezone.utc),
    )


def test_chunks_document_with_overlap_and_provenance() -> None:
    document = make_document("abcdefghij")

    chunks = DocumentChunkingService().chunk_document(
        document,
        chunk_size=4,
        overlap=1,
    )

    assert [chunk.content for chunk in chunks] == [
        "abcd",
        "defg",
        "ghij",
    ]
    assert [chunk.chunk_index for chunk in chunks] == [0, 1, 2]
    assert [
        (chunk.start_offset, chunk.end_offset)
        for chunk in chunks
    ] == [(0, 4), (3, 7), (6, 10)]
    assert all(chunk.document_id == document.document_id for chunk in chunks)
    assert all(chunk.relative_path == document.relative_path for chunk in chunks)


def test_chunk_size_larger_than_document_returns_one_chunk() -> None:
    document = make_document("short")

    chunks = DocumentChunkingService().chunk_document(
        document,
        chunk_size=100,
        overlap=10,
    )

    assert len(chunks) == 1
    assert chunks[0].content == "short"
    assert chunks[0].start_offset == 0
    assert chunks[0].end_offset == 5


def test_empty_document_returns_no_chunks() -> None:
    assert DocumentChunkingService().chunk_document(make_document("")) == []


@pytest.mark.parametrize(
    ("chunk_size", "overlap", "message"),
    [
        (0, 0, "chunk_size must be greater than zero"),
        (-1, 0, "chunk_size must be greater than zero"),
        (10, -1, "overlap must not be negative"),
        (10, 10, "overlap must be smaller than chunk_size"),
        (10, 11, "overlap must be smaller than chunk_size"),
    ],
)
def test_invalid_configuration_raises_error(
    chunk_size: int,
    overlap: int,
    message: str,
) -> None:
    with pytest.raises(ChunkingError, match=message):
        DocumentChunkingService().chunk_document(
            make_document("content"),
            chunk_size=chunk_size,
            overlap=overlap,
        )
