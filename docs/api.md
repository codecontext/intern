# Intern API

## 1. Purpose

The API is the stable boundary between the browser and Intern's backend.

The frontend should communicate through HTTP APIs and should not depend on internal implementation details such as Ollama, embeddings, vector stores, or retrieval algorithms.

---

# 2. API Principles

The API should:

* Use explicit request/response models.
* Validate input using Pydantic.
* Return predictable error responses.
* Keep infrastructure details hidden.
* Remain usable if backend infrastructure changes.
* Support future multiple clients.

---

# 3. Health

```http
GET /api/health
```

Example response:

```json
{
  "status": "ok"
}
```

Future health information may include component status.

---

# 4. Models

```http
GET /api/models
```

Returns locally available LLM models.

Example:

```json
{
  "models": [
    {
      "name": "gemma3:4b"
    },
    {
      "name": "qwen3:4b"
    }
  ]
}
```

The frontend should not assume a fixed model list.

---

# 5. Conversations

```http
GET    /api/conversations
POST   /api/conversations
GET    /api/conversations/{id}
PATCH  /api/conversations/{id}
DELETE /api/conversations/{id}
```

---

# 6. Messages

```http
POST /api/conversations/{id}/messages
```

Conceptual request:

```json
{
  "content": "Explain this architecture",
  "model": "qwen3:4b"
}
```

The API should eventually support:

* Knowledge-base selection
* Internet mode
* Streaming
* Tool execution
* Agent mode

---

# 7. Knowledge Bases

```http
GET    /api/knowledge-bases
POST   /api/knowledge-bases
GET    /api/knowledge-bases/{id}
DELETE /api/knowledge-bases/{id}
```

Future operations:

```http
POST /api/knowledge-bases/{id}/index
POST /api/knowledge-bases/{id}/refresh
GET  /api/knowledge-bases/{id}/sources
```

---

# 8. Search

Future retrieval API:

```http
POST /api/search
```

Example:

```json
{
  "knowledge_base_id": "project-a",
  "query": "Where is DMA configured?"
}
```

---

# 9. Agent

Future endpoint:

```http
POST /api/agent
```

The request may eventually contain:

```json
{
  "goal": "Investigate the failing I2C test",
  "knowledge_base_id": "project-a"
}
```

Agent execution should be permission-aware.

---

# 10. Streaming

Long-running LLM operations should eventually support streaming.

Possible implementation:

```text
Browser
   ↓
HTTP streaming
   ↓
FastAPI
   ↓
LLM provider
```

The exact transport should be selected based on actual requirements.

---

# 11. Error Handling

Errors should be explicit.

Conceptual response:

```json
{
  "error": {
    "code": "MODEL_UNAVAILABLE",
    "message": "The selected model is unavailable."
  }
}
```

Internal exception details should not be exposed unnecessarily.

---

# 12. API Versioning

Versioning should only be introduced when there is an actual compatibility requirement.

Avoid adding versioning complexity prematurely.

---

# 13. API Boundary Rule

The browser should know:

```text
What operation is available
What request is required
What response is returned
```

The browser should not know:

```text
How Ollama works
How embeddings work
How vector search works
How documents are chunked
How agents select tools
```
