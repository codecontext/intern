# Intern Ingestion

## 1. Purpose

Ingestion converts external project information into normalized, searchable knowledge.

---

# 2. Pipeline

```text
Source Folder
     ↓
File Discovery
     ↓
File Filtering
     ↓
Parser
     ↓
Normalized Content
     ↓
Chunking
     ↓
Metadata
     ↓
Embeddings
     ↓
Vector Store
```

---

# 3. File Discovery

Discovery should:

* Walk configured directories.
* Identify supported files.
* Ignore configured exclusions.
* Avoid indexing generated artifacts unnecessarily.
* Preserve source paths.

Potential exclusions:

```text
.git/
build/
out/
node_modules/
venv/
__pycache__/
```

The exact exclusion policy should be configurable.

---

# 4. Parsing

Different content types may use different parsers.

```text
PDF       → PDF parser
Markdown  → Markdown parser
JSON      → Structured parser
Python    → Code-aware parser
C/C++     → Code-aware parser
Text      → Plain-text parser
```

The parser should produce normalized content rather than directly writing to the vector store.

---

# 5. Normalized Document

Conceptually:

```text
Document
├── source
├── content
├── metadata
└── document_type
```

---

# 6. Error Handling

A failure to parse one file should not necessarily stop the entire ingestion operation.

The system should record:

```text
File
Status
Error
```

and continue where appropriate.

---

# 7. Incremental Ingestion

Future implementations should detect:

```text
New files
Modified files
Deleted files
Unchanged files
```

Unchanged files should ideally not be reprocessed.

---

# 8. Images

Image ingestion may eventually use:

```text
OCR
Vision models
Image metadata
Multimodal embeddings
```

This should be introduced only when there is a concrete requirement.

---

# 9. Security

The ingestion system must treat source files as potentially sensitive.

It should not upload project data externally unless the user explicitly enables an external service.
