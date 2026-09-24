import ollama

from .base import LLM


class OllamaLLM(LLM):
    """Ollama-based local language model provider."""

    def list_models(self) -> list[str]:
        response = ollama.list()

        return [
            model.model
            for model in response.models
        ]

    def chat(self, model: str, messages: list[dict[str, str]]) -> str:
        response = ollama.chat(
            model=model,
            messages=messages,
        )

        return response.message.content
