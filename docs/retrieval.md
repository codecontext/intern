# Intern Retrieval

## 1. Purpose

Retrieval finds relevant knowledge for a user query.

Retrieval is the bridge between the knowledge base and RAG.

---

# 2. Basic Flow

```text
Question
 ↓
Query Processing
 ↓
Query Embedding
 ↓
Vector Search
 ↓
Candidate Chunks
 ↓
Ranking
 ↓
Relevant Context
```

---

# 3. Top-K Retrieval

The initial implementation may retrieve a configurable number of candidates:

```text
Top K
```

The correct value should be determined experimentally.

More results do not necessarily mean better answers.

---

# 4. Metadata Filtering

Retrieval may use metadata:

```text
knowledge_base
file type
language
path
symbol
project
```

---

# 5. Hybrid Search

Engineering repositories often benefit from both:

```text
Semantic retrieval
```

and:

```text
Exact keyword/identifier search
```

Future hybrid retrieval may combine both.

---

# 6. Reranking

Initial retrieval may produce:

```text
20 candidate chunks
```

A reranker can reduce these to:

```text
5 highly relevant chunks
```

Potential future pipeline:

```text
Vector Search
     ↓
Keyword Search
     ↓
Merge Candidates
     ↓
Reranker
     ↓
Top Results
```

---

# 7. Source Information

Every retrieved result should retain its source.

Example:

```text
drivers/i2c/i2c_dw.c
docs/dma.md
tests/i2c/test_dma.c
```

Future UI should allow users to inspect the source.

---

# 8. Retrieval Quality

Retrieval should be evaluated separately from generation.

Useful metrics may include:

```text
Precision
Recall
Hit Rate
MRR
```

For an engineering assistant, qualitative evaluation with real project questions is also important.

---

# 9. Failure Cases

Retrieval may fail because:

* Relevant file was not indexed.
* Chunk boundaries are poor.
* Query lacks important terminology.
* Embedding model is unsuitable.
* Metadata filters are incorrect.
* Relevant information exists outside the knowledge base.

The system should avoid pretending that retrieval succeeded when it did not.
