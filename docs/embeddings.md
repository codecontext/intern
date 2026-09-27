# Intern Embeddings

## 1. Purpose

Embeddings convert text or other supported content into numerical vectors that represent semantic characteristics.

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

---

# 2. Query Embeddings

A user query follows the same process:

```text
Question
 ↓
Embedding Model
 ↓
Query Vector
 ↓
Vector Search
```

---

# 3. Generation vs Embedding

These are separate concerns.

```text
Generation Model
    ↓
Answer generation

Embedding Model
    ↓
Search representation
```

The same model does not need to perform both tasks.

---

# 4. Local-First

The preferred embedding architecture is local:

```text
Intern
 ↓
Local Embedding Model
 ↓
Vector
```

Project content should not leave the local environment merely to create embeddings.

---

# 5. Model Selection

Embedding models should be selected based on:

* Retrieval quality
* Language support
* Code support
* Resource consumption
* Embedding dimensions
* Local hardware requirements
* License

The generation model and embedding model should remain independently configurable.

---

# 6. Vector Compatibility

Changing embedding models may invalidate an existing vector index.

Therefore, vector metadata should identify the embedding configuration.

Conceptually:

```text
embedding_model
embedding_dimension
embedding_version
```

---

# 7. Future

Potential improvements:

* Code embeddings
* Multilingual embeddings
* Multimodal embeddings
* Model benchmarking
* Embedding caching
