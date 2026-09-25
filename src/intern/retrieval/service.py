from collections.abc import Sequence

from intern.embeddings.service import EmbeddingService
from intern.retrieval.models import RetrievedChunk
from intern.vectorstore.base import VectorStore


class RetrievalError(ValueError):
    """Raised when a retrieval request is invalid."""


class RetrievalService:
    """Retrieve relevant document chunks for a text query."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self._embedding_service = embedding_service
        self._vector_store = vector_store

    def retrieve(
        self,
        query: str,
        embedding_model: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        if not query.strip():
            raise RetrievalError("Query must not be empty")

        if not embedding_model.strip():
            raise RetrievalError("Embedding model must not be empty")

        if top_k <= 0:
            raise RetrievalError("top_k must be greater than zero")

        query_embedding = self._embedding_service.embed_text(
            model=embedding_model,
            text=query,
        )
        results = self._vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return [
            RetrievedChunk(
                chunk_id=result.chunk_id,
                chunk=result.chunk,
                score=result.score,
            )
            for result in results
        ]

    @staticmethod
    def assemble_context(chunks: Sequence[RetrievedChunk]) -> str:
        """Format retrieved chunks for a future prompt/context assembly step."""
        return "\n\n".join(
            f"[Source: {item.chunk.relative_path}]\n{item.chunk.content}"
            for item in chunks
        )