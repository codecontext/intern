from abc import ABC, abstractmethod


class LLM(ABC):
    """Interface for language model providers."""

    @abstractmethod
    def list_models(self) -> list[str]:
        """Return models available from the provider."""
        raise NotImplementedError

    @abstractmethod
    def chat(self, model: str, messages: list[dict[str, str]]) -> str:
        """Generate a response using the selected model."""
        raise NotImplementedError
