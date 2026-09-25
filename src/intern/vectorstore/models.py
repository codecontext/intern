from dataclasses import dataclass
from uuid import UUID

from intern.chunking.models import DocumentChunk


@dataclass(frozen=True)
class VectorSearchResult:
    """A stored chunk and its similarity to a query vector."""

    chunk_id: UUID
    chunk: DocumentChunk
    score: float
