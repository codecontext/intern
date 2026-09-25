from uuid import uuid4

from intern.chunking.models import DocumentChunk
from intern.ingestion.models import Document


class ChunkingError(ValueError):
    """Raised when chunking configuration is invalid."""


class DocumentChunkingService:
    """Split complete documents into deterministic character-based chunks."""

    def chunk_document(
        self,
        document: Document,
        chunk_size: int = 1_000,
        overlap: int = 100,
    ) -> list[DocumentChunk]:
        """Return ordered chunks while preserving source offsets and metadata."""
        self._validate_configuration(chunk_size, overlap)

        chunks: list[DocumentChunk] = []
        start_offset = 0
        chunk_index = 0

        while start_offset < len(document.content):
            end_offset = min(start_offset + chunk_size, len(document.content))
            chunks.append(
                DocumentChunk(
                    chunk_id=uuid4(),
                    document_id=document.document_id,
                    source_path=document.source_path,
                    relative_path=document.relative_path,
                    chunk_index=chunk_index,
                    start_offset=start_offset,
                    end_offset=end_offset,
                    content=document.content[start_offset:end_offset],
                )
            )
            chunk_index += 1

            if end_offset == len(document.content):
                break

            start_offset = end_offset - overlap

        return chunks

    @staticmethod
    def _validate_configuration(chunk_size: int, overlap: int) -> None:
        if chunk_size <= 0:
            raise ChunkingError("chunk_size must be greater than zero")

        if overlap < 0:
            raise ChunkingError("overlap must not be negative")

        if overlap >= chunk_size:
            raise ChunkingError("overlap must be smaller than chunk_size")
