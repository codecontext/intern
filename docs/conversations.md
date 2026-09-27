# Intern Conversation Management

## 1. Purpose

Conversation management represents the user's interaction history independently from the LLM provider and knowledge base.

---

# 2. Core Model

A conversation contains:

```text
conversation_id
created_at
updated_at
title
messages[]
```

A message contains:

```text
message_id
role
content
created_at
```

Initial roles:

```text
user
assistant
```

Future roles may include:

```text
system
tool
```

---

# 3. Separation from Knowledge Base

Conversation history:

```text
"What did we discuss earlier?"
```

Knowledge base:

```text
"Information contained in the project repository."
```

They should remain separate.

---

# 4. Conversation Lifecycle

```text
Create
  ↓
Add messages
  ↓
Update
  ↓
List
  ↓
Retrieve
  ↓
Rename
  ↓
Delete
```

---

# 5. Context Construction

A future request may use:

```text
Current user message
+
Relevant conversation history
+
Retrieved knowledge
+
Internet results
+
Tool results
```

Conversation history should not automatically mean that every historical message is sent to the LLM indefinitely.

Context management may eventually require:

* Message limits
* Summarization
* Context trimming
* Token budgeting

---

# 6. Persistence

The browser should not be the authoritative owner of conversations.

The backend should own conversation state.

This allows:

* Multiple clients
* Persistent history
* Search
* Server-side context management
* Future authentication

---

# 7. Titles

Conversation titles may initially be generated from the first user message.

Future implementations may use the LLM to generate concise titles.

---

# 8. Search

Future conversation search may support:

```text
Title
Message content
Date
Knowledge base
```

This should be introduced only when required.

---

# 9. Conversation and Knowledge Base

A conversation may optionally reference a knowledge base:

```text
Conversation
     │
     └── Knowledge Base reference
```

The knowledge base itself remains reusable across conversations.
