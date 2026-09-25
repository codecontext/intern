from dataclasses import dataclass
from uuid import UUID

from intern.chunking.models import DocumentChunk


@dataclass(frozen=True)
class RetrievedChunk:
    """A retrieved chunk with its relevance score."""

    chunk_id: UUID
    chunk: DocumentChunk
    score: float