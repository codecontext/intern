from collections.abc import Sequence
import math
from uuid import UUID

from intern.embeddings.models import EmbeddedChunk
from intern.vectorstore.base import VectorStore
from intern.vectorstore.models import VectorSearchResult


class VectorStoreError(ValueError):
    """Raised when vector-store input is invalid."""


class InMemoryVectorStore(VectorStore):
    """Store vectors in memory and search them with cosine similarity."""

    def __init__(self) -> None:
        self._chunks: dict[UUID, EmbeddedChunk] = {}

    def upsert(self, chunks: Sequence[EmbeddedChunk]) -> None:
        for embedded_chunk in chunks:
            if not embedded_chunk.embedding:
                raise VectorStoreError("Embedding vectors must not be empty")

            self._chunks[embedded_chunk.chunk.chunk_id] = embedded_chunk

    def search(
        self,
        query_embedding: Sequence[float],
        top_k: int = 5,
    ) -> list[VectorSearchResult]:
        if top_k <= 0:
            raise VectorStoreError("top_k must be greater than zero")

        if not query_embedding:
            raise VectorStoreError("Query embedding must not be empty")

        results = []
        for embedded_chunk in self._chunks.values():
            if len(embedded_chunk.embedding) != len(query_embedding):
                raise VectorStoreError("Embedding dimensions must match")

            score = self._cosine_similarity(
                embedded_chunk.embedding,
                query_embedding,
            )
            results.append(
                VectorSearchResult(
                    chunk_id=embedded_chunk.chunk.chunk_id,
                    chunk=embedded_chunk.chunk,
                    score=score,
                )
            )

        results.sort(key=lambda result: (-result.score, str(result.chunk_id)))
        return results[:top_k]

    def count(self) -> int:
        return len(self._chunks)

    @staticmethod
    def _cosine_similarity(
        left: Sequence[float],
        right: Sequence[float],
    ) -> float:
        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))

        if left_norm == 0 or right_norm == 0:
            return 0.0

        dot_product = sum(
            left_value * right_value
            for left_value, right_value in zip(left, right)
        )
        return dot_product / (left_norm * right_norm)
