from typing import Protocol


class ContextProvider(Protocol):
    """Provide retrieved context for a user query."""

    def context_for(self, query: str) -> str:
        """Return relevant context or an empty string."""
        ...
