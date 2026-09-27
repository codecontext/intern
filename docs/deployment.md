# Intern Deployment

## 1. Purpose

Intern is designed to evolve from a developer workstation application into an internal engineering service.

---

# 2. Development Deployment

```text
Developer PC
├── Browser
├── FastAPI
├── Ollama
├── Embedding Model
└── Vector Store
```

All major components can initially run locally.

---

# 3. Internal Demo

```text
Engineering LAN

          ┌──────────────┐
          │    Browser   │
          └──────┬───────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Internal Server │
        │                 │
        │ FastAPI         │
        │ LLM Runtime     │
        │ Embeddings      │
        │ Vector Store    │
        └─────────────────┘
```

---

# 4. Production Direction

Future architecture:

```text
Users
  ↓
Internal Web Application
  ↓
API Layer
  ↓
Application Services
  ├── Authentication
  ├── Conversations
  ├── Knowledge Bases
  ├── Retrieval
  ├── Agents
  └── Tools
  ↓
AI / Storage Infrastructure
```

---

# 5. Browser/API Boundary

The browser should continue to communicate with Intern through the API.

Deployment changes should not require redesigning the frontend.

---

# 6. Configuration

Environment-specific configuration should be externalized.

Examples:

```text
LLM endpoint
Embedding model
Vector store path
Knowledge-base root
Logging level
Authentication settings
```

Secrets should never be committed to source control.

---

# 7. Local-First Requirement

A basic Intern installation should remain usable without:

```text
Cloud AI
Paid APIs
Hosted vector databases
External authentication services
```

---

# 8. Scaling

Scaling should be introduced only when required.

Potential future requirements:

```text
Multiple users
Concurrent inference
Large knowledge bases
GPU inference
Distributed storage
Authentication
```

Only then should more complex infrastructure be evaluated.

---

# 9. Backup

Future persistent deployments should define backup strategies for:

```text
Conversations
Knowledge-base metadata
Vector indexes
Configuration
Audit records
```

Original project source files should generally remain owned by their existing source-control/storage systems.
