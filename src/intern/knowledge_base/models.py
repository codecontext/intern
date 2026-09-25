from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID

from intern.ingestion.models import Document


@dataclass(frozen=True)
class KnowledgeBase:
    """An in-memory knowledge base backed by local files and folders."""

    knowledge_base_id: UUID
    source_paths: tuple[Path, ...]
    documents: tuple[Document, ...]
    created_at: datetime
