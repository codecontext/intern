from datetime import datetime, timezone
from collections.abc import Sequence
from pathlib import Path
from uuid import UUID, uuid4

from intern.ingestion.service import DocumentIngestionService
from intern.knowledge_base.models import KnowledgeBase


class KnowledgeBaseNotFoundError(LookupError):
    """Raised when a knowledge base ID is not present."""


class KnowledgeBaseService:
    """Create and inspect in-memory knowledge bases from local sources."""

    def __init__(
        self,
        ingestion_service: DocumentIngestionService | None = None,
    ) -> None:
        self._ingestion_service = ingestion_service or DocumentIngestionService()
        self._knowledge_bases: dict[UUID, KnowledgeBase] = {}

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
        self._knowledge_bases.clear()
        self._knowledge_bases[knowledge_base.knowledge_base_id] = knowledge_base
        return knowledge_base

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
