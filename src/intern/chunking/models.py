from dataclasses import dataclass
from pathlib import Path
from uuid import UUID


@dataclass(frozen=True)
class DocumentChunk:
    """A text window from an ingested document with source provenance."""

    chunk_id: UUID
    document_id: UUID
    source_path: Path
    relative_path: Path
    chunk_index: int
    start_offset: int
    end_offset: int
    content: str
