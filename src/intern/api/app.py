from fastapi import FastAPI

from intern.application.chat import ChatService
from intern.llm.ollama import OllamaLLM


app = FastAPI(
    title="Intern",
    description="Context-aware knowledge assistant",
    version="0.1.0",
)


chat_service = ChatService(
    llm=OllamaLLM(),
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/models")
def models() -> list[str]:
    return chat_service.list_models()


@app.post("/api/chat")
def chat(
    model: str,
    messages: list[dict[str, str]],
) -> dict[str, str]:
    response = chat_service.chat(
        model=model,
        messages=messages,
    )

    return {
        "response": response,
    }
