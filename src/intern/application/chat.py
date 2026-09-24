from intern.llm.base import LLM


class ChatService:
    """Application service for chat operations."""

    def __init__(self, llm: LLM):
        self._llm = llm

    def list_models(self) -> list[str]:
        return self._llm.list_models()

    def chat(
        self,
        model: str,
        messages: list[dict[str, str]],
    ) -> str:
        return self._llm.chat(
            model=model,
            messages=messages,
        )
