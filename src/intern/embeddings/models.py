from dataclasses import dataclass

from intern.chunking.models import DocumentChunk


@dataclass(frozen=True)
class EmbeddedChunk:
    """A chunk paired with its embedding vector."""

    chunk: DocumentChunk
    embedding: tuple[float, ...]
