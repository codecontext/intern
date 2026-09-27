# Intern Architecture

## 1. Purpose

This document describes the internal architecture of **Intern**, a local-first, context-aware AI knowledge assistant for software and engineering teams.

The architecture is designed to evolve incrementally:

```text
Local LLM
    ↓
Conversation Management
    ↓
Knowledge Base
    ↓
RAG
    ↓
Internet Retrieval
    ↓
Tool Use
    ↓
Agentic Workflows
```

The architecture prioritizes:

* Clear subsystem boundaries
* Replaceable infrastructure
* Local-first execution
* Testability
* Explicit context sources
* Evidence-based answers
* Human-controlled actions
* Small incremental changes

---

# 2. High-Level Architecture

```text
                         ┌─────────────────┐
                         │     Browser     │
                         └────────┬────────┘
                                  │ HTTP
                                  ▼
                         ┌─────────────────┐
                         │    FastAPI      │
                         │      API        │
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │  Application    │
                         │    Services     │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
       Conversation          Knowledge Base       Agent
       Management             / Retrieval       Orchestration
              │                   │                   │
              │                   ▼                   ▼
              │             Ingestion / RAG         Tools
              │                   │
              │                   ▼
              │             Vector Store
              │
              └───────────────────┬───────────────────┘
                                  │
                                  ▼
                           LLM Abstraction
                                  │
                                  ▼
                               Ollama
                                  │
                                  ▼
                              Local LLM
```

The browser communicates only with the application API.

Infrastructure details such as Ollama, embeddings, vector stores, and retrieval implementations should remain behind application-level interfaces.

---

# 3. Architectural Layers

## 3.1 Web Layer

Responsible for:

* Browser UI
* User interaction
* Rendering conversations
* Selecting models
* Selecting knowledge bases
* Displaying retrieval/activity information

The web layer should not contain business logic.

---

## 3.2 API Layer

Responsible for:

* HTTP endpoints
* Request validation
* Response models
* Authentication integration in the future
* Mapping HTTP requests to application services

The API layer should not directly communicate with Ollama or the vector store.

---

## 3.3 Application Layer

Responsible for application use cases.

Examples:

```text
Create conversation
Send message
List conversations
Select knowledge base
Search knowledge
Generate answer
Run agent task
Request tool execution
```

The application layer coordinates domain operations without depending directly on infrastructure implementations.

---

## 3.4 Infrastructure Layer

Infrastructure includes:

```text
Ollama
Embedding models
Vector stores
File systems
Web search providers
Databases
External services
```

Infrastructure should be accessed through interfaces or adapters where practical.

---

# 4. Source Contexts

Intern should explicitly distinguish several context sources:

```text
LLM Knowledge
Conversation Context
Knowledge Base
Internet Information
Tool Results
Agent Observations
```

These sources should not be silently mixed.

A future response pipeline may conceptually be:

```text
User Message
      │
      ├── Conversation Context
      │
      ├── Knowledge Base
      │
      ├── Internet
      │
      └── Tools
             │
             ▼
       Context Assembly
             │
             ▼
            LLM
             │
             ▼
          Response
```

---

# 5. Knowledge Modes

The application should support explicit context controls:

| Knowledge Base | Internet | Behaviour                        |
| -------------- | -------- | -------------------------------- |
| OFF            | OFF      | LLM knowledge only               |
| ON             | OFF      | LLM + local knowledge            |
| OFF            | ON       | LLM + internet                   |
| ON             | ON       | LLM + local knowledge + internet |

Additional controls may later exist for tools and agents.

---

# 6. Package Boundaries

```text
src/intern/

├── api/
├── application/
├── chunking/
├── embeddings/
├── ingestion/
├── knowledge_base/
├── llm/
├── retrieval/
├── vectorstore/
└── web/
```

Responsibilities:

| Package          | Responsibility                |
| ---------------- | ----------------------------- |
| `api`            | HTTP/API boundary             |
| `application`    | Application use cases         |
| `chunking`       | Document/code chunking        |
| `embeddings`     | Vector generation             |
| `ingestion`      | File discovery and processing |
| `knowledge_base` | KB lifecycle                  |
| `llm`            | LLM provider abstraction      |
| `retrieval`      | Search and retrieval          |
| `vectorstore`    | Persistent vector storage     |
| `web`            | Browser interface             |

Future packages may include:

```text
agents/
tools/
permissions/
authentication/
```

These should be introduced only when required.

---

# 7. Dependency Direction

The preferred dependency direction is:

```text
Web
 ↓
API
 ↓
Application
 ↓
Interfaces
 ↓
Infrastructure
```

Application logic should not depend directly on:

```text
Ollama API
Specific vector database
Specific embedding model
Specific web-search provider
```

Instead:

```text
Application
     ↓
LLM Interface
     ↓
Ollama Adapter
```

and:

```text
Application
     ↓
Vector Store Interface
     ↓
Vector Store Implementation
```

---

# 8. Replaceability

Components should be replaceable when the abstraction is justified.

Examples:

```text
Ollama
   ↓
LLM interface
   ↓
Another local provider
```

```text
Vector Store A
   ↓
VectorStore interface
   ↓
Vector Store B
```

Avoid creating abstractions merely for theoretical future requirements.

---

# 9. Current vs Future Architecture

The current system is intentionally smaller than the long-term architecture.

### Current

```text
Browser
   ↓
FastAPI
   ↓
Application
   ↓
LLM abstraction
   ↓
Ollama
   ↓
Local LLM
```

### Planned

```text
Browser
   ↓
FastAPI
   ↓
Application Services
   ├── Conversations
   ├── Knowledge Base
   ├── Retrieval
   └── RAG
        ↓
      LLM
```

### Future

```text
Application
   ├── RAG
   ├── Internet Retrieval
   ├── Agent Orchestration
   └── Tool System
              ↓
       Controlled Engineering Tools
```

---

# 10. Architectural Constraints

Intern should:

* Prefer local execution.
* Keep external services optional.
* Keep application logic provider-independent.
* Keep conversation and knowledge-base state separate.
* Avoid premature distributed infrastructure.
* Keep core logic testable without external services.
* Require explicit authorization for consequential actions.

---

# 11. Architecture Decision Rule

Before introducing a new subsystem, ask:

1. What problem does it solve?
2. Which existing subsystem owns that responsibility?
3. Does it introduce unnecessary infrastructure?
4. Can it be tested independently?
5. Can the implementation be replaced later?
6. Does it preserve the existing API boundary?
7. Is it required now or only theoretically useful later?

The simplest architecture that satisfies the current requirement should be preferred.
