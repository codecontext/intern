from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from intern.application.chat import ChatService
from intern.llm.ollama import OllamaLLM


WEB_DIR = Path(__file__).resolve().parents[1] / "web"


app = FastAPI(
    title="Intern",
    description="Context-aware knowledge assistant",
    version="0.1.0",
)


app.mount(
    "/static",
    StaticFiles(directory=WEB_DIR),
    name="static",
)


chat_service = ChatService(
    llm=OllamaLLM(),
)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(
        WEB_DIR / "index.html"
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
