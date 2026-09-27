# Intern LLM Architecture

## 1. Purpose

The LLM subsystem provides language-model capabilities to Intern while keeping the rest of the application independent of a specific provider.

---

# 2. Architecture

```text
Application
     ↓
LLM Interface
     ↓
Provider Adapter
     ↓
Ollama
     ↓
Local Model
```

---

# 3. Responsibilities

The LLM subsystem is responsible for:

* Model discovery
* Model selection
* Prompt submission
* Response generation
* Streaming
* Provider errors
* Provider-specific configuration

It should not be responsible for:

* Conversation persistence
* Knowledge-base management
* Retrieval
* File ingestion
* Agent orchestration

---

# 4. Provider Abstraction

Conceptually:

```python
class LLM:
    def generate(...):
        ...

    def stream(...):
        ...

    def list_models(...):
        ...
```

The exact interface should evolve with actual requirements.

---

# 5. Ollama

Ollama is the current local LLM runtime.

Example models:

```text
gemma3:4b
qwen3:4b
deepseek-r1:7b
```

Model availability depends on the host machine.

The application must not assume that any particular model is installed.

---

# 6. Model Selection

Model selection should be runtime-configurable.

```text
Browser
   ↓
Selected model
   ↓
API
   ↓
LLM service
   ↓
Ollama
```

The model should not be hard-coded into application business logic.

---

# 7. Prompt Construction

Prompt construction belongs to the application/LLM boundary rather than the Ollama adapter.

The provider adapter should primarily handle provider communication.

Future prompt construction may incorporate:

```text
System instructions
Conversation history
Retrieved context
Internet results
Tool results
User message
```

---

# 8. Streaming

Streaming should allow partial responses to reach the browser.

```text
LLM
 ↓
Token/chunk stream
 ↓
Application
 ↓
API
 ↓
Browser
```

The streaming implementation should not leak provider-specific behavior into the frontend.

---

# 9. Errors

Potential errors:

```text
Provider unavailable
Model unavailable
Request timeout
Invalid model
Generation failure
Malformed provider response
```

These should be translated into application-level errors.

---

# 10. Embeddings

Embeddings are intentionally separate from generation.

```text
Generation Model
        ≠
Embedding Model
```

Intern should be able to use different models for these tasks.

---

# 11. Future Providers

Potential future providers include:

```text
Another local runtime
Internal company inference server
Other self-hosted model runtime
```

Adding a provider should not require rewriting application services.
