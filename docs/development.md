# Intern Development Guide

## 1. Purpose

This document defines the development workflow and engineering conventions for Intern.

Intern is both a software project and a learning project. Implementation should remain understandable and incremental.

---

# 2. Development Principles

### Small Changes

Each change should solve one clear problem.

Prefer:

```text
Add conversation repository
```

over:

```text
Add conversation repository + database + authentication + caching + API redesign
```

---

### Explicit Code

Prefer simple, readable implementations over unnecessary abstraction.

---

### Testability

Core logic should not require:

* Ollama
* Internet access
* GPU
* Browser
* External services

during unit testing.

---

# 3. Development Workflow

Recommended workflow:

```text
1. Understand requirement
2. Read relevant documentation
3. Inspect existing implementation
4. Identify smallest change
5. Implement
6. Add/update tests
7. Run tests
8. Review architecture impact
9. Commit
```

---

# 4. Documentation Before Implementation

Before implementing a subsystem:

```text
README.md
    ↓
architecture.md
    ↓
Relevant subsystem document
    ↓
Implementation
```

For example, before implementing retrieval:

```text
README.md
architecture.md
retrieval.md
rag.md
```

should be consulted.

---

# 5. Project Structure

```text
intern/
├── README.md
├── pyproject.toml
├── .env.example
├── docs/
├── src/
│   └── intern/
└── tests/
```

---

# 6. Python Code Organization

Application code belongs under:

```text
src/intern/
```

Tests belong under:

```text
tests/
```

Avoid placing application modules at repository root.

---

# 7. Configuration

Configuration should be externalized where appropriate.

Example:

```text
.env
```

should contain local configuration.

The repository should contain:

```text
.env.example
```

but not secrets.

---

# 8. Dependencies

Add dependencies only when they provide clear value.

Before adding a package, consider:

* Is the functionality actually required?
* Can the standard library solve the problem?
* Does the package add significant complexity?
* Is it actively maintained?
* Does it work with local-first requirements?

---

# 9. Testing

Run relevant tests after every meaningful change.

Typical commands:

```bash
pytest
```

For focused testing:

```bash
pytest tests/path/to/test_file.py
```

---

# 10. Commit Strategy

Commits should represent coherent changes.

Examples:

```text
Add conversation domain model
```

```text
Add Ollama LLM adapter
```

```text
Add knowledge base lifecycle service
```

```text
Add retrieval interface
```

Avoid vague messages such as:

```text
changes
update
fix stuff
work
```

---

# 11. AI Coding Assistants

AI coding assistants should:

1. Read `README.md`.
2. Read the relevant documentation.
3. Inspect existing code.
4. Make the smallest required change.
5. Avoid unrelated refactoring.
6. Add tests.
7. Explain architectural implications.
8. Leave unrelated future functionality untouched.

AI-generated code should not automatically introduce:

```text
Microservices
Kubernetes
Message queues
Complex databases
Agent frameworks
Cloud APIs
```

unless explicitly justified.

---

# 12. Definition of Done

A feature is generally complete when:

* Required functionality exists.
* Relevant tests exist.
* Existing tests still pass.
* Documentation is updated when architecture changes.
* No unrelated files were modified.
* No unnecessary dependency was introduced.
* The implementation follows existing package boundaries.
* The change is understandable to another developer.

---

# 13. Refactoring Rule

Do not combine major refactoring with unrelated feature work unless the refactoring is required for the feature.

Prefer:

```text
Commit 1
Add required interface

Commit 2
Implement feature

Commit 3
Refactor if necessary
```

over one large change.

---

# 14. Learning Principle

Intern should make architectural concepts visible.

When introducing a technology, document:

```text
Why it exists
What problem it solves
How it works
What it depends on
What depends on it
How it is tested
What alternatives exist
```

This is especially important for:

* Embeddings
* Vector databases
* RAG
* Retrieval
* Agents
* Tool calling
* Permission systems
