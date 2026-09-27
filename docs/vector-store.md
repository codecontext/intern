# Intern Vector Store

## 1. Purpose

The vector store persists embedded knowledge and provides similarity search.

---

# 2. Stored Information

A vector record may contain:

```text
id
vector
content
metadata
```

Metadata may include:

```text
knowledge_base_id
source_path
file_type
chunk_id
language
symbol
line_start
line_end
```

---

# 3. Operations

The vector store should conceptually support:

```text
insert()
update()
delete()
search()
count()
```

Knowledge-base lifecycle operations may require:

```text
delete_by_knowledge_base()
```

---

# 4. Search

Basic semantic search:

```text
Query
 ↓
Query Vector
 ↓
Vector Store
 ↓
Top-K Results
```

---

# 5. Metadata Filtering

Search may eventually support:

```text
knowledge_base_id = X
language = C++
file_type = source
```

This is important for engineering repositories.

---

# 6. Hybrid Retrieval

Future retrieval may combine:

```text
Vector Search
+
Keyword Search
+
Metadata Filtering
+
Reranking
```

This is useful because engineering questions often contain exact identifiers.

Example:

```text
DMA_Channel_3
```

may be better handled by exact matching than semantic similarity alone.

---

# 7. Abstraction

Application logic should not depend directly on one vector-store implementation.

Conceptually:

```text
Retrieval Service
      ↓
VectorStore interface
      ↓
Implementation
```

---

# 8. Local Deployment

The initial implementation should prefer a simple local vector store.

A distributed vector database should only be introduced if scale or multi-user requirements justify it.
