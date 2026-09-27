# Intern

**Intern** is a local-first, context-aware AI knowledge assistant designed to help people **ask questions, find information, retrieve documents, understand knowledge, and work with their own data**.

It combines a locally running Large Language Model (LLM) with conversation context, user-provided knowledge, document retrieval, internet access, and eventually controlled tools and agentic workflows.

Intern is intended to be useful for **individuals, teams, and organizations across different domains**. It can work with general information as well as specialized knowledge such as business documents, technical documentation, project files, policies, procedures, research material, source code, reports, manuals, and other organizational knowledge.

The project starts as a simple local AI assistant and progressively evolves into a context-aware knowledge platform.

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

---

## 1. Vision

The goal of Intern is to build a **private, extensible, context-aware AI assistant** that can work with information supplied by the user or organization.

Instead of relying only on the knowledge contained in a language model, Intern can progressively combine multiple sources of context:

```text
                    ┌─────────────────────┐
                    │    User Question    │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      Conversation        Knowledge Base      Internet
        Context             Documents         Retrieval
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                         Context / RAG
                               │
                               ▼
                            LLM
                               │
                               ▼
                            Answer
```

Over time, the system can evolve from answering questions to performing controlled tasks using tools.

---

## 2. Why Intern?

A general-purpose AI model is useful, but it does not automatically understand the specific information available to a person or organization.

Important information may exist in:

* Documents
* PDFs
* Markdown files
* Spreadsheets
* Reports
* Presentations
* Images
* Manuals
* Policies
* Project files
* Source code
* Configuration files
* Research material
* Internal documentation
* Databases
* Websites
* Other organizational knowledge

Intern provides a framework for connecting this information to an AI assistant.

The objective is to move from:

```text
"What does the AI model know?"
```

towards:

```text
"What information is available to me,
and how can the AI help me understand and use it?"
```

---

## 3. Core Capabilities

Intern is designed around several progressively connected capabilities.

### 3.1 Conversational AI

Users can interact with the assistant using natural language.

The assistant maintains conversation context so that users can ask follow-up questions without repeatedly providing the same information.

---

### 3.2 Knowledge Base

Users can provide a folder or collection of information that Intern can process and make available to the AI.

For example:

```text
Knowledge Base
├── Documents
├── Reports
├── Manuals
├── Notes
├── Policies
├── Research
├── Project Files
└── Other Data
```

The knowledge base is separate from the language model itself.

---

### 3.3 Retrieval-Augmented Generation

Intern can retrieve relevant information from the knowledge base before generating an answer.

```text
Question
   ↓
Search Knowledge
   ↓
Relevant Information
   ↓
Context
   ↓
LLM
   ↓
Answer
```

This allows answers to be grounded in user-provided information rather than relying exclusively on the model's built-in knowledge.

---

### 3.4 Internet Retrieval

Intern can optionally retrieve information from the internet.

The internet is treated as a separate context source rather than being silently mixed with local knowledge.

This allows users to control whether an answer should use:

```text
Local Knowledge
Internet
Both
Neither
```

---

### 3.5 Tool Use

Intern can eventually interact with controlled tools to perform useful operations.

Examples include:

* Searching files
* Reading documents
* Finding information
* Comparing documents
* Searching websites
* Inspecting structured data
* Running calculations
* Querying databases
* Running approved processes
* Performing domain-specific operations

Tools should be explicitly defined and permission-controlled.

---

### 3.6 Agentic Workflows

The long-term direction is to allow Intern to perform multi-step tasks.

For example:

```text
User Request
     ↓
Understand Task
     ↓
Search Knowledge
     ↓
Retrieve Information
     ↓
Inspect Additional Sources
     ↓
Use Appropriate Tools
     ↓
Combine Results
     ↓
Return Result
```

Agentic behavior should remain observable and controlled rather than becoming an unrestricted autonomous system.

---

# 4. Context Sources

Intern can progressively combine several sources of context.

```text
                    ┌────────────────────┐
                    │   User Question    │
                    └─────────┬──────────┘
                              │
       ┌──────────┬───────────┼───────────┬───────────┐
       ▼          ▼           ▼           ▼           ▼
 Conversation  Knowledge   Internet     Tools      Future
   Context      Base      Retrieval    Results     Sources
       │          │           │           │           │
       └──────────┴───────────┼───────────┴───────────┘
                              ▼
                       Context Assembly
                              │
                              ▼
                             LLM
                              │
                              ▼
                           Response
```

Possible context sources include:

1. **LLM knowledge**
2. **Conversation context**
3. **Knowledge-base content**
4. **Internet information**
5. **Tool results**
6. **Agent observations**

---

# 5. Knowledge Modes

Intern should provide explicit control over which information sources are used.

| Knowledge Base | Internet | Behavior                         |
| -------------- | -------- | -------------------------------- |
| OFF            | OFF      | LLM only                         |
| ON             | OFF      | LLM + local knowledge            |
| OFF            | ON       | LLM + internet                   |
| ON             | ON       | LLM + local knowledge + internet |

This makes the source of information predictable and controllable.

---

# 6. High-Level Architecture

The initial architecture is intentionally simple.

```text
┌──────────────────────────────┐
│          Browser             │
│       Web Interface          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          FastAPI             │
│          API Layer           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Application Layer       │
│                              │
│ Conversation                │
│ Knowledge                   │
│ Retrieval                   │
│ RAG                         │
│ Internet                    │
│ Tools                       │
│ Agent Orchestration         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       AI Infrastructure      │
│                              │
│ LLM                         │
│ Embeddings                  │
│ Vector Store                │
└──────────────────────────────┘
```

The architecture is modular so that individual components can evolve independently.

---

# 7. Current Application Layer

The initial implementation follows a simple request flow:

```text
Browser
   ↓
FastAPI API
   ↓
Application Services
   ↓
LLM Abstraction
   ↓
Ollama
   ↓
Local LLM
```

This keeps the initial system easy to understand while leaving room for future capabilities.

---

# 8. Technology Stack

The initial technology stack is intentionally lightweight.

### Backend

* Python 3.11+
* FastAPI
* Uvicorn
* Pydantic

### Frontend

* HTML
* CSS
* JavaScript

A large frontend framework is intentionally avoided during the early stages.

### Local AI

* Ollama
* Locally hosted open models

Examples may include:

* Gemma
* Qwen
* DeepSeek
* Other compatible models

The model should be selectable at runtime rather than hard-coded into the application.

### Future AI Components

Potential future components include:

* Local embedding models
* Vector storage
* Document parsers
* Code-aware processing
* Metadata filtering
* Hybrid retrieval
* Reranking
* Tool execution
* Agent orchestration

---

# 9. Project Structure

The project is organized around clear responsibilities.

```text
intern/
│
├── README.md
│
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── docs/
│   ├── architecture.md
│   ├── development.md
│   ├── roadmap.md
│   ├── api.md
│   ├── llm.md
│   ├── conversations.md
│   ├── knowledge-base.md
│   ├── ingestion.md
│   ├── chunking.md
│   ├── embeddings.md
│   ├── vector-store.md
│   ├── retrieval.md
│   ├── rag.md
│   ├── internet-retrieval.md
│   ├── agents.md
│   ├── tools.md
│   ├── permissions.md
│   ├── testing.md
│   ├── deployment.md
│   └── security.md
│
├── src/
│   └── intern/
│       ├── application/
│       ├── api/
│       ├── chunking/
│       ├── embeddings/
│       ├── ingestion/
│       ├── knowledge_base/
│       ├── llm/
│       ├── retrieval/
│       ├── vectorstore/
│       └── web/
│
└── tests/
```

---

# 10. Major Components

## API

Responsible for exposing application functionality through HTTP APIs.

Examples:

```text
/api/health
/api/models
/api/conversations
/api/conversations/{id}
/api/conversations/{id}/messages
/api/knowledge-bases
/api/search
/api/agent
```

---

## Application

Contains application-level use cases and orchestration.

It should coordinate components without containing low-level implementation details.

---

## LLM

Provides an abstraction over language-model providers.

The application should not depend directly on a specific model.

```text
Application
     ↓
LLM Interface
     ↓
Ollama
     ↓
Selected Model
```

This makes it possible to change models without redesigning the application.

---

## Knowledge Base

Responsible for managing collections of information that can be used by Intern.

A knowledge base may represent:

* Personal documents
* Team information
* Organizational information
* A particular project
* Research material
* A subject or topic
* Any other user-selected information collection

---

## Ingestion

Responsible for discovering and processing source material.

```text
Selected Source
      ↓
File Discovery
      ↓
Document Parsing
      ↓
Content Extraction
      ↓
Chunking
      ↓
Metadata
      ↓
Embedding
      ↓
Vector Store
```

---

## Chunking

Large documents need to be divided into smaller retrievable units.

For general documents, chunking may consider:

* Paragraphs
* Sections
* Headings
* Pages
* Tables
* Logical boundaries

For structured or source material, specialized chunking can eventually consider:

* Functions
* Classes
* Symbols
* Interfaces
* Configuration sections
* Other logical structures

---

## Embeddings

Embeddings convert information into vector representations.

```text
Document
   ↓
Chunks
   ↓
Embedding Model
   ↓
Vectors
```

The embedding model is independent from the generation model.

---

## Vector Store

Stores:

* Embeddings
* Original content
* Source information
* Metadata

Example metadata:

```text
source
file_path
file_type
chunk_index
section
page
project
language
symbol
```

The vector store can eventually support:

* Semantic search
* Keyword search
* Metadata filtering
* Hybrid retrieval
* Reranking

---

# 11. Retrieval-Augmented Generation

RAG is one of the central capabilities of Intern.

```text
             User Question
                   │
                   ▼
            Query Processing
                   │
                   ▼
              Retrieval
                   │
                   ▼
           Relevant Chunks
                   │
                   ▼
          Optional Reranking
                   │
                   ▼
          Context Construction
                   │
                   ▼
                  LLM
                   │
                   ▼
                Answer
```

The system should ideally preserve information about where retrieved content originated so that answers can eventually provide evidence or source references.

---

# 12. Document and Information Support

Intern should not assume that all knowledge is plain text.

Different information types require different processing strategies.

Potential sources include:

```text
Documents
├── PDF
├── Markdown
├── Text
├── Word documents
├── Spreadsheets
├── Presentations
└── Other documents

Structured Data
├── JSON
├── CSV
├── Database records
└── Other structured sources

Technical / Project Data
├── Source code
├── Configuration
├── Logs
├── Build output
└── Project documentation

Visual Information
├── Images
├── Scanned documents
├── Diagrams
└── Other visual material
```

The system should use appropriate parsers and processing methods rather than treating every source as plain text.

---

# 13. Internet Retrieval

Internet retrieval is an optional context source.

```text
User Question
      │
      ├──────────────► Local Knowledge
      │
      └──────────────► Internet
                            │
                            ▼
                         Results
                            │
                            ▼
                     Context Assembly
```

Internet content should be treated as external information and should not automatically override trusted local information.

Future implementations should also consider:

* Source attribution
* Freshness
* Relevance
* Trust
* Conflicting information
* Untrusted web content

---

# 14. Conversations

Conversation state is separate from the knowledge base.

A conversation can contain:

```text
conversation_id
created_at
updated_at
messages[]
```

A message initially contains:

```text
role
content
```

Initial roles:

```text
user
assistant
```

The backend remains authoritative for conversation state.

Future capabilities may include:

* Conversation persistence
* Conversation listing
* Rename
* Delete
* Search
* Multiple conversations
* Multiple users
* Server-side context management
* Multiple clients

---

# 15. Tool System

Tools allow the AI to interact with information and controlled capabilities.

Potential tools include:

```text
search_knowledge_base()
search_documents()
search_code()
read_file()
list_files()
search_symbol()
find_references()
compare_files()
search_web()
query_database()
run_calculation()
run_tests()
inspect_configuration()
inspect_logs()
build_project()
```

The exact tool set will evolve according to real use cases.

Tools should have:

* Clearly defined inputs
* Clearly defined outputs
* Permission boundaries
* Error handling
* Auditability
* Observable execution

---

# 16. Agentic Direction

Intern should evolve gradually toward agentic behavior.

The progression is:

```text
LLM
 ↓
Conversation
 ↓
Knowledge
 ↓
RAG
 ↓
Tool Use
 ↓
Agent
```

An agent should be able to:

1. Understand a request
2. Determine what information is required
3. Search available sources
4. Select appropriate tools
5. Inspect results
6. Perform additional steps when necessary
7. Produce a final response

The objective is not unrestricted autonomy.

The objective is **useful, observable, controlled automation**.

---

# 17. Human Control

Intern should keep people in control of consequential operations.

A simple permission model can distinguish between operations such as:

### Lower-risk operations

```text
Search
Read
Retrieve
List
Compare
Analyze
```

### Controlled operations

```text
Run tests
Build
Query systems
Access external sources
```

### Higher-risk operations

```text
Modify files
Delete files
Execute arbitrary commands
Change configurations
Perform external actions
```

Higher-risk operations should require explicit authorization.

The user should be able to understand what the system is doing.

For example:

```text
Searching knowledge base...
Found 6 relevant documents.

Reading relevant sections...
Found supporting information.

Comparing two documents...

Preparing answer...
```

These are observable actions, not hidden reasoning.

---

# 18. Local-First Strategy

A fundamental design principle is **local-first operation**.

The basic system should not require:

* Paid AI APIs
* Cloud-hosted LLMs
* Proprietary vector databases
* Mandatory external services

The initial architecture can run entirely on a local machine:

```text
┌───────────────────────────────┐
│       User's Computer         │
│                               │
│ Browser                       │
│    ↓                          │
│ FastAPI                       │
│    ↓                          │
│ Ollama                        │
│    ↓                          │
│ Local LLM                     │
│                               │
│ Local Embeddings              │
│ Local Vector Store            │
│ Local Knowledge               │
└───────────────────────────────┘
```

This provides a strong foundation for privacy, experimentation, and offline development.

---

# 19. Deployment Evolution

Intern can evolve through several deployment stages.

## Stage 1 — Personal Development

```text
Developer Computer
├── Browser
├── FastAPI
├── Ollama
├── LLM
├── Embeddings
└── Vector Store
```

---

## Stage 2 — Internal Usage

```text
Users
   ↓
Internal Network
   ↓
Web Application
   ↓
Internal Server
   ├── FastAPI
   ├── LLM
   ├── Embeddings
   └── Vector Store
```

---

## Stage 3 — Organization Platform

```text
Users
   ↓
Web Application
   ↓
API
   ├── Authentication
   ├── Conversations
   ├── Knowledge
   ├── Retrieval
   ├── Agents
   └── Tools
          ↓
    AI Infrastructure
          ↓
    Storage / Knowledge
```

The architecture should evolve only when real requirements justify additional infrastructure.

---

# 20. Development Philosophy

Intern should be developed incrementally.

Each feature should:

1. Solve a clear problem
2. Have a defined boundary
3. Be easy to test
4. Avoid unnecessary dependencies
5. Keep existing functionality working
6. Be understandable by a developer reading the code later

The project should favor **simple working systems over premature complexity**.

---

# 21. Avoid Premature Infrastructure

The early project should avoid introducing infrastructure simply because it may be useful later.

Examples:

* Kubernetes
* Microservices
* Distributed queues
* Distributed vector databases
* Complex frontend frameworks
* Cloud AI APIs
* Multi-agent architectures
* Autonomous code modification
* Complex authentication
* Distributed caching

These may become appropriate later if actual requirements justify them.

The initial objective is to understand and build the fundamental system.

---

# 22. Testing

Testing should exist at multiple levels.

### Unit Tests

Test individual components without external services.

Examples:

```text
Chunking
Metadata extraction
Prompt construction
Conversation logic
Retrieval logic
Validation
```

### Integration Tests

Test interactions between components.

Examples:

```text
API → Application
Application → LLM
Ingestion → Embeddings
Retrieval → Vector Store
```

### End-to-End Tests

Test complete user workflows.

```text
User
 ↓
Browser
 ↓
API
 ↓
Application
 ↓
LLM
 ↓
Response
```

Core application logic should remain testable without requiring Ollama, internet access, GPU hardware, or a browser.

External dependencies should be replaceable with mocks or test implementations.

---

# 23. Security and Privacy

Because Intern may process private information, security is an important part of the architecture.

Important areas include:

* Local data protection
* Authentication
* Authorization
* Knowledge-base isolation
* Secret management
* Tool permissions
* Network exposure
* External data trust
* Auditability
* File access control

External information, especially web content, should be treated as **untrusted input**.

The AI should not automatically treat instructions found inside retrieved documents or web pages as trusted commands.

Consequential operations should require appropriate permissions.

---

# 24. Extensibility

Intern should not be tightly coupled to a single model, storage engine, embedding model, or retrieval implementation.

For example:

```text
                ┌── Ollama
                ├── Future LLM Provider
                └── Future Local Runtime
                         │
Application ─── LLM Interface
                         │
                ┌────────┴────────┐
                │                 │
          Embedding Interface   Retrieval
                │                 │
          Local Model         Vector Store
```

This allows the implementation to evolve without redesigning the entire application.

---

# 25. Roadmap

The roadmap is intentionally incremental.

### Phase 1 — Basic Assistant

```text
✓ Local LLM
✓ Browser interface
✓ FastAPI backend
✓ Model selection
✓ Basic conversation
```

### Phase 2 — Conversation Management

```text
Conversation persistence
Conversation history
Multiple conversations
Context management
```

### Phase 3 — Knowledge Base

```text
Folder selection
File discovery
Document processing
Content extraction
```

### Phase 4 — RAG

```text
Chunking
Embeddings
Vector storage
Semantic retrieval
Context construction
Source references
```

### Phase 5 — Internet

```text
Web retrieval
Source handling
Freshness
External-context management
```

### Phase 6 — Tools

```text
File tools
Search tools
Data tools
Controlled execution
Permissions
```

### Phase 7 — Agents

```text
Task planning
Multi-step execution
Tool selection
Observation
Controlled automation
```

### Phase 8 — Internal Platform

```text
Multi-user support
Authentication
Knowledge isolation
Centralized deployment
Auditability
Administration
```

---

# 26. Documentation

Detailed design information is maintained separately from this README.

| Document                | Purpose                                       |
| ----------------------- | --------------------------------------------- |
| `architecture.md`       | Overall system architecture                   |
| `development.md`        | Development practices and project conventions |
| `roadmap.md`            | Feature evolution                             |
| `api.md`                | API design                                    |
| `llm.md`                | LLM integration                               |
| `conversations.md`      | Conversation architecture                     |
| `knowledge-base.md`     | Knowledge-base design                         |
| `ingestion.md`          | Information ingestion                         |
| `chunking.md`           | Chunking strategies                           |
| `embeddings.md`         | Embedding architecture                        |
| `vector-store.md`       | Vector storage                                |
| `retrieval.md`          | Retrieval architecture                        |
| `rag.md`                | RAG pipeline                                  |
| `internet-retrieval.md` | Internet information retrieval                |
| `agents.md`             | Agent architecture                            |
| `tools.md`              | Tool system                                   |
| `permissions.md`        | Permission model                              |
| `testing.md`            | Testing strategy                              |
| `deployment.md`         | Deployment architecture                       |
| `security.md`           | Security and privacy                          |

The README provides the **overall product and architectural picture**.

The detailed documents provide the implementation-level design.

---

# 27. Design Principles

Intern follows several core principles.

### Local First

Prefer local execution and local data whenever practical.

### Context Aware

The assistant should use the information relevant to the user's request.

### User Controlled

Users should control what information and capabilities are available.

### Source Aware

The system should distinguish between different sources of information.

### Modular

Major capabilities should be replaceable and independently testable.

### Incremental

Build simple capabilities before introducing complex infrastructure.

### Observable

Important system actions should be visible to the user.

### Secure

Private information and consequential operations require appropriate protection.

### General Purpose

The architecture should support different users, domains, information types, and workflows.

---

# 28. Long-Term Vision

The long-term goal is to build an AI system that can work as a **personal or organizational knowledge layer**.

Instead of being only a chatbot, Intern should progressively become a system that can:

```text
Understand
    ↓
Search
    ↓
Retrieve
    ↓
Reason over information
    ↓
Use tools
    ↓
Perform controlled tasks
```

It should be able to work with the information that matters to the user while keeping the user in control of the available knowledge, external access, and actions.

The project therefore evolves through:

```text
Chatbot
   ↓
Knowledge Assistant
   ↓
RAG Assistant
   ↓
Tool-Using Assistant
   ↓
Context-Aware AI Assistant
   ↓
Controlled AI Agent
```

The central idea remains simple:

> **Give people a private AI assistant that can understand, retrieve, and work with the information that matters to them.**
