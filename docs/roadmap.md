# Intern Roadmap

## 1. Purpose

This document describes the conceptual evolution of Intern.

The roadmap is directional rather than a fixed schedule.

Features should be implemented only when their dependencies and actual requirements justify them.

---

# 2. Evolution

```text
Chatbot
   ↓
Knowledge Assistant
   ↓
RAG Assistant
   ↓
Tool-Using Assistant
   ↓
Engineering Agent
```

---

# 3. Phase 1 — Chat Foundation

Goal:

Build a clean local LLM chat application.

```text
Browser
   ↓
FastAPI
   ↓
Application Service
   ↓
LLM Abstraction
   ↓
Ollama
```

Capabilities:

* Chat interface
* Model selection
* Basic conversation
* Streaming responses
* Health endpoint
* Basic API contracts

---

# 4. Phase 2 — Conversation Management

Add persistent conversation concepts.

Capabilities:

* Conversation creation
* Conversation listing
* Conversation selection
* Message history
* Conversation renaming
* Conversation deletion
* Server-side conversation state

---

# 5. Phase 3 — Knowledge Base

Introduce reusable project context.

Capabilities:

* Select folder
* Create knowledge base
* Remove knowledge base
* Track indexed sources
* Display indexing status

---

# 6. Phase 4 — Ingestion

Introduce document processing.

```text
Files
 ↓
Discovery
 ↓
Parsing
 ↓
Normalization
 ↓
Chunking
```

Initially support a small set of useful formats.

Additional formats should be added based on actual requirements.

---

# 7. Phase 5 — Embeddings

Introduce local embeddings.

```text
Chunk
 ↓
Embedding Model
 ↓
Vector
```

Query:

```text
Question
 ↓
Embedding Model
 ↓
Query Vector
```

---

# 8. Phase 6 — Vector Retrieval

Introduce persistent vector storage.

Capabilities:

* Store vectors
* Store metadata
* Similarity search
* Metadata filtering
* Source identification

---

# 9. Phase 7 — RAG

Combine:

```text
Question
 ↓
Retrieval
 ↓
Relevant Context
 ↓
Prompt Construction
 ↓
LLM
 ↓
Evidence-Based Answer
```

Add source references to retrieved information.

---

# 10. Phase 8 — Code-Aware Knowledge

Improve engineering repository understanding.

Potential capabilities:

* Symbol extraction
* Function-aware chunking
* Class-aware chunking
* Language detection
* Line ranges
* File relationships
* Search by symbol
* Search by path

---

# 11. Phase 9 — Internet Retrieval

Add controlled external retrieval.

Capabilities:

* Explicit web-search mode
* Source collection
* Content extraction
* Source attribution
* Separation between internal and external information

---

# 12. Phase 10 — Tools

Introduce controlled engineering tools.

Potential tools:

```text
read_file()
list_files()
search_code()
search_symbol()
find_references()
compare_files()
run_tests()
run_static_analysis()
inspect_git_history()
```

---

# 13. Phase 11 — Agents

Introduce iterative workflows.

```text
Goal
 ↓
Decide
 ↓
Tool
 ↓
Observe
 ↓
Decide
 ↓
Tool
 ↓
...
 ↓
Result
```

The initial agent should be read-only where possible.

---

# 14. Phase 12 — Permissions

Introduce explicit approval.

Examples:

```text
Read file        → automatic
Search repository → automatic
Run test          → controlled
Run build         → controlled
Modify file       → explicit approval
Delete file       → explicit approval
```

---

# 15. Phase 13 — Internal Deployment

Evolve from:

```text
Developer PC
```

to:

```text
Internal Linux Server
        ↓
Engineering LAN
        ↓
Multiple Browser Clients
```

Potential additions:

* Authentication
* Authorization
* User isolation
* Knowledge-base ownership
* Administrative controls
* Usage monitoring

---

# 16. Guiding Rule

Do not implement a later phase merely because it appears on the roadmap.

The roadmap describes direction.

Actual implementation should be driven by:

```text
Requirement
    +
Current architecture
    +
Dependencies
    +
Learning objective
```
