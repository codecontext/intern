from collections.abc import Sequence

from intern.chunking.models import DocumentChunk
from intern.embeddings.base import EmbeddingProvider
from intern.embeddings.models import EmbeddedChunk


class EmbeddingError(RuntimeError):
    """Raised when embedding generation cannot produce valid results."""


class EmbeddingService:
    """Map provider-generated vectors back to their source chunks."""

    def __init__(self, provider: EmbeddingProvider):
        self._provider = provider

    def embed_chunks(
        self,
        model: str,
        chunks: Sequence[DocumentChunk],
    ) -> list[EmbeddedChunk]:
        if not model.strip():
            raise EmbeddingError("Embedding model must not be empty")

        if not chunks:
            return []

        vectors = self._provider.embed(
            model=model,
            texts=[chunk.content for chunk in chunks],
        )

        if len(vectors) != len(chunks):
            raise EmbeddingError(
                "Embedding provider returned a different number of vectors "
                "than input chunks"
            )

        return [
            EmbeddedChunk(
                chunk=chunk,
                embedding=tuple(vector),
            )
            for chunk, vector in zip(chunks, vectors)
        ]
