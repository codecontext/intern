from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from intern.ingestion.models import Document


class IngestionError(ValueError):
    """Raised when a source directory cannot be ingested."""


class DocumentIngestionService:
    """Discover and read supported local documents without transforming them."""

    SUPPORTED_EXTENSIONS = frozenset(
        {
            ".c",
            ".cpp",
            ".css",
            ".csv",
            ".go",
            ".html",
            ".java",
            ".js",
            ".json",
            ".md",
            ".py",
            ".rs",
            ".sh",
            ".sql",
            ".ts",
            ".tsx",
            ".txt",
            ".yaml",
            ".yml",
        }
    )

    def ingest_directory(self, directory: Path) -> list[Document]:
        """Read supported files recursively in deterministic path order."""
        source_directory = directory.expanduser().resolve()

        if not source_directory.exists():
            raise IngestionError(f"Source directory does not exist: {directory}")

        if not source_directory.is_dir():
            raise IngestionError(f"Source path is not a directory: {directory}")

        documents = []
        for path in sorted(source_directory.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            documents.append(self._read_document(source_directory, path))

        return documents

    def ingest_path(self, path: Path) -> list[Document]:
        """Read one supported file or all supported files in a directory."""
        source_path = path.expanduser().resolve()

        if source_path.is_dir():
            return self.ingest_directory(source_path)

        if not source_path.exists():
            raise IngestionError(f"Source path does not exist: {path}")

        if source_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise IngestionError(
                f"Unsupported document type: {source_path.name}"
            )

        return [self._read_document(source_path.parent, source_path)]

    def _read_document(self, source_directory: Path, path: Path) -> Document:
        try:
            content = path.read_text(encoding="utf-8")
            metadata = path.stat()
        except OSError as error:
            raise IngestionError(f"Could not read document: {path}") from error
        except UnicodeDecodeError as error:
            raise IngestionError(f"Document is not valid UTF-8 text: {path}") from error

        return Document(
            document_id=uuid4(),
            source_path=path,
            relative_path=path.relative_to(source_directory),
            filename=path.name,
            extension=path.suffix.lower(),
            content=content,
            size_bytes=metadata.st_size,
            modified_at=datetime.fromtimestamp(
                metadata.st_mtime,
                tz=timezone.utc,
            ),
        )
