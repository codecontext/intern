from datetime import datetime, timezone
from collections.abc import Sequence
from pathlib import Path
from typing import Callable
from uuid import UUID, uuid4

from intern.chunking.service import DocumentChunkingService
from intern.embeddings.models import EmbeddedChunk
from intern.embeddings.service import EmbeddingService
from intern.ingestion.service import DocumentIngestionService
from intern.knowledge_base.models import KnowledgeBase
from intern.retrieval.service import RetrievalService
from intern.vectorstore.base import VectorStore


class KnowledgeBaseNotFoundError(LookupError):
    """Raised when a knowledge base ID is not present."""


class KnowledgeBaseIndexingError(RuntimeError):
    """Raised when Knowledge Base embeddings cannot be generated."""


class KnowledgeBaseService:
    """Create and inspect in-memory knowledge bases from local sources."""

    def __init__(
        self,
        ingestion_service: DocumentIngestionService | None = None,
        chunking_service: DocumentChunkingService | None = None,
        embedding_service: EmbeddingService | None = None,
        embedding_model: str = "",
        vector_store_factory: Callable[[], VectorStore] | None = None,
    ) -> None:
        self._ingestion_service = ingestion_service or DocumentIngestionService()
        self._chunking_service = chunking_service or DocumentChunkingService()
        self._embedding_service = embedding_service
        self._embedding_model = embedding_model
        self._vector_store_factory = vector_store_factory
        self._knowledge_bases: dict[UUID, KnowledgeBase] = {}
        self._retrieval_service: RetrievalService | None = None

    def create(self, source_paths: Sequence[Path]) -> KnowledgeBase:
        if not source_paths:
            raise ValueError("At least one source path is required")

        normalized_paths = tuple(
            path.expanduser().resolve() for path in source_paths
        )
        documents = []
        seen_paths: set[Path] = set()

        for path in normalized_paths:
            for document in self._ingestion_service.ingest_path(path):
                if document.source_path not in seen_paths:
                    documents.append(document)
                    seen_paths.add(document.source_path)

        knowledge_base = KnowledgeBase(
            knowledge_base_id=uuid4(),
            source_paths=normalized_paths,
            documents=tuple(documents),
            created_at=datetime.now(timezone.utc),
        )
        try:
            self._build_index(documents)
        except Exception as error:
            raise KnowledgeBaseIndexingError(
                "Knowledge Base indexing failed. Check the embedding model "
                "and Ollama service."
            ) from error
        self._knowledge_bases.clear()
        self._knowledge_bases[knowledge_base.knowledge_base_id] = knowledge_base
        return knowledge_base

    def _build_index(self, documents: Sequence) -> None:
        self._retrieval_service = None

        if (
            self._embedding_service is None
            or not self._embedding_model.strip()
            or self._vector_store_factory is None
        ):
            return

        chunks = [
            chunk
            for document in documents
            for chunk in self._chunking_service.chunk_document(document)
        ]
        embedded_chunks = self._embedding_service.embed_chunks(
            model=self._embedding_model,
            chunks=chunks,
        )
        vector_store = self._vector_store_factory()
        vector_store.upsert(embedded_chunks)
        self._retrieval_service = RetrievalService(
            self._embedding_service,
            vector_store,
        )

    def context_for(self, query: str, top_k: int = 5) -> str:
        """Retrieve indexed Knowledge Base context for a user query."""
        if self._retrieval_service is None:
            return ""

        chunks = self._retrieval_service.retrieve(
            query=query,
            embedding_model=self._embedding_model,
            top_k=top_k,
        )
        return self._retrieval_service.assemble_context(chunks)

    def validate_paths(self, source_paths: Sequence[Path]) -> None:
        """Validate all sources without creating a knowledge base."""
        if not source_paths:
            raise ValueError("At least one source path is required")

        for path in source_paths:
            self._ingestion_service.ingest_path(path)

    def get(self, knowledge_base_id: UUID) -> KnowledgeBase:
        knowledge_base = self._knowledge_bases.get(knowledge_base_id)

        if knowledge_base is None:
            raise KnowledgeBaseNotFoundError(str(knowledge_base_id))

        return knowledge_base

    def list(self) -> list[KnowledgeBase]:
        return list(self._knowledge_bases.values())
