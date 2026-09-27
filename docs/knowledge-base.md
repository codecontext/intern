# Intern Knowledge Base

## 1. Purpose

A knowledge base represents a reusable collection of project-specific information available for retrieval.

Examples:

```text
Firmware Project
Automotive ECU Project
SoC Documentation
Test Repository
Architecture Documentation
```

---

# 2. Knowledge Base Lifecycle

```text
Create
  ↓
Select source
  ↓
Discover files
  ↓
Ingest
  ↓
Index
  ↓
Retrieve
  ↓
Refresh
  ↓
Delete
```

---

# 3. Source Folder

A knowledge base may initially be associated with a local folder:

```text
~/projects/my-project/
```

The system should record the configured source rather than copying unnecessary data.

---

# 4. Sources

Potential sources:

```text
Source code
PDF
Markdown
Text
Configuration
Logs
Test files
Images
Specifications
```

---

# 5. Metadata

Each indexed item should preserve useful metadata.

Minimum metadata:

```text
knowledge_base_id
source_path
file_name
file_type
chunk_id
```

Potential future metadata:

```text
language
symbol
class
function
line_start
line_end
section
page
project
```

---

# 6. Isolation

Knowledge bases should be logically isolated.

Retrieval from one knowledge base should not accidentally return content from another.

Future multi-user deployment must also consider user ownership and access control.

---

# 7. Refresh

The system should eventually support incremental refresh.

Conceptually:

```text
Existing files
      +
Changed files
      +
New files
      -
Deleted files
      ↓
Updated index
```

A complete rebuild may remain available as a simpler fallback.

---

# 8. Status

The UI should eventually expose states such as:

```text
Not indexed
Indexing
Ready
Partially indexed
Failed
Refreshing
```

---

# 9. Knowledge Base vs Conversation

Knowledge base:

```text
Reusable project information
```

Conversation:

```text
Interaction history
```

The same knowledge base may be used by multiple conversations.
