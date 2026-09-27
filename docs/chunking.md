# Intern Chunking

## 1. Purpose

Chunking divides source material into units suitable for retrieval and embedding.

Good chunking is important because retrieval quality depends heavily on the quality and meaning of individual chunks.

---

# 2. General Documents

Document chunking may consider:

```text
Heading
Section
Paragraph
Page
Document boundaries
```

Avoid splitting content in ways that destroy semantic meaning.

---

# 3. Source Code

Source code should eventually use structure-aware chunking.

Example:

```text
file.c
 ├── includes
 ├── macros
 ├── struct
 ├── function_a()
 ├── function_b()
 └── function_c()
```

A function should ideally remain a coherent retrieval unit.

---

# 4. Metadata

Code chunks may contain:

```text
file
language
symbol
function
class
namespace
line_start
line_end
```

---

# 5. Chunk Size

Chunk size should not be selected purely by character count.

Potential factors:

* Semantic boundaries
* Token count
* File type
* Code structure
* Retrieval requirements

---

# 6. Overlap

Text chunks may use overlap where necessary.

```text
Chunk A
──────────────
       overlap
       ──────────────
       Chunk B
```

Overlap should be justified rather than automatically applied everywhere.

---

# 7. Future Improvements

Potential approaches:

* AST-aware chunking
* Symbol-aware chunking
* Parent-child chunks
* Hierarchical retrieval
* Function + surrounding context
* Documentation/code relationship metadata
