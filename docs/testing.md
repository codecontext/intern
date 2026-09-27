# Intern Testing Strategy

## 1. Purpose

Testing should verify both individual components and complete workflows.

---

# 2. Testing Levels

```text
Unit Tests
    ↓
Integration Tests
    ↓
End-to-End Tests
```

---

# 3. Unit Tests

Unit tests should test individual components independently.

Examples:

```text
Conversation service
Prompt construction
Chunker
Metadata extraction
Retriever
Tool schema
Permission evaluator
```

External dependencies should be mocked or replaced.

---

# 4. Integration Tests

Examples:

```text
API → Application Service

Application → LLM Adapter

Ingestion → Chunking → Embedding

Retrieval → Context Construction
```

---

# 5. End-to-End Tests

Example:

```text
Open application
 ↓
Create conversation
 ↓
Ask question
 ↓
Receive response
```

Future RAG workflow:

```text
Create KB
 ↓
Index files
 ↓
Ask question
 ↓
Retrieve evidence
 ↓
Generate answer
 ↓
Display source
```

---

# 6. External Dependencies

Tests should not require:

```text
Internet
GPU
Ollama
Production vector store
```

unless explicitly classified as integration tests.

---

# 7. Retrieval Evaluation

RAG requires evaluation beyond normal unit testing.

Questions:

```text
Was the relevant document retrieved?
Was the relevant chunk retrieved?
Were irrelevant chunks retrieved?
Was source metadata preserved?
```

Potential metrics:

```text
Recall
Precision
Hit Rate
MRR
```

---

# 8. Agent Testing

Agent workflows should test:

```text
Correct tool selection
Tool failure handling
Permission handling
Termination
Iteration limits
Unexpected tool output
```

---

# 9. Safety Testing

Test that:

* Unauthorized tools cannot execute.
* Disabled internet mode does not perform web searches.
* One knowledge base cannot retrieve another's data.
* Destructive operations require approval.
* Tool errors do not bypass permission checks.

---

# 10. Regression Testing

Every bug discovered in production or development should, where practical, result in a regression test.

---

# 11. Test Philosophy

Tests should verify behaviour rather than implementation details wherever practical.
