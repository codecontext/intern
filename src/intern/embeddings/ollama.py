from collections.abc import Sequence

import ollama

from intern.embeddings.base import EmbeddingProvider


class OllamaEmbeddingProvider(EmbeddingProvider):
    """Generate local embeddings through Ollama's embed endpoint."""

    def embed(self, model: str, texts: Sequence[str]) -> list[list[float]]:
        if not texts:
            return []

        response = ollama.embed(
            model=model,
            input=list(texts),
        )

        return [list(vector) for vector in response.embeddings]
