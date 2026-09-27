# Intern Retrieval-Augmented Generation

## 1. Purpose

RAG allows Intern to answer questions using project-specific information that is not contained in the LLM's pretrained knowledge.

---

# 2. Basic Architecture

```text
User Question
      ↓
Query Processing
      ↓
Retrieval
      ↓
Relevant Chunks
      ↓
Context Construction
      ↓
LLM
      ↓
Answer
```

---

# 3. Context Sources

RAG context may eventually include:

```text
Knowledge Base
Conversation
Internet Results
Tool Results
```

Each source should remain identifiable.

---

# 4. Context Construction

Retrieved information should be converted into structured LLM context.

Conceptually:

```text
System Instructions

Conversation Context

Retrieved Evidence:
[Source A]
...

[Source B]
...

User Question
```

---

# 5. Evidence

A RAG answer should ideally identify supporting sources.

Example:

```text
The I2C driver uses DMA for transfers.

Sources:
- drivers/i2c/i2c_dw.c
- drivers/dma/dma_dw.c
- docs/dma.md
```

The exact citation mechanism can evolve.

---

# 6. Grounding

The system should distinguish:

```text
Retrieved fact
Model interpretation
General model knowledge
```

The LLM should not be instructed to treat every generated statement as retrieved fact.

---

# 7. No-Answer / Insufficient Evidence

If retrieval does not provide enough information, the system should be able to say that the available knowledge base does not contain sufficient evidence.

This is preferable to fabricating project-specific information.

---

# 8. RAG Pipeline

A complete future pipeline may be:

```text
Question
   ↓
Query Analysis
   ↓
Conversation Context
   ↓
Knowledge Retrieval
   ↓
Internet Retrieval
   ↓
Candidate Ranking
   ↓
Context Assembly
   ↓
Prompt Construction
   ↓
LLM
   ↓
Answer + Sources
```

Not every request needs every stage.

---

# 9. Knowledge Modes

RAG should respect:

```text
Knowledge Base: ON/OFF
Internet: ON/OFF
```

If both are disabled:

```text
Question
 ↓
Conversation Context
 ↓
LLM
```

No external retrieval should occur.

---

# 10. Evaluation

RAG should be evaluated independently of the LLM.

Questions include:

```text
Did retrieval find the correct file?
Did retrieval find the correct function?
Was the relevant context included?
Did the answer correctly use the evidence?
```

---

# 11. Future RAG Capabilities

Potential improvements:

* Hybrid retrieval
* Reranking
* Hierarchical retrieval
* Code-aware retrieval
* Query expansion
* Source citations
* Confidence indicators
* Retrieval debugging
