from abc import ABC, abstractmethod
from collections.abc import Sequence


class EmbeddingProvider(ABC):
    """Interface for local or remote text embedding providers."""

    @abstractmethod
    def embed(self, model: str, texts: Sequence[str]) -> list[list[float]]:
        """Return one embedding vector for each input text."""
        raise NotImplementedError
