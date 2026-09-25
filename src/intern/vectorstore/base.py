from abc import ABC, abstractmethod
from collections.abc import Sequence

from intern.embeddings.models import EmbeddedChunk
from intern.vectorstore.models import VectorSearchResult


class VectorStore(ABC):
    """Interface for storing embedded document chunks and searching vectors."""

    @abstractmethod
    def upsert(self, chunks: Sequence[EmbeddedChunk]) -> None:
        """Insert or replace embedded chunks by chunk ID."""
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query_embedding: Sequence[float],
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        """Return the most similar stored chunks."""
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """Return the number of stored chunks."""
        raise NotImplementedError
