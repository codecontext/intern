from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID


@dataclass(frozen=True)
class Document:
    """A complete ingested file and its source metadata."""

    document_id: UUID
    source_path: Path
    relative_path: Path
    filename: str
    extension: str
    content: str
    size_bytes: int
    modified_at: datetime
