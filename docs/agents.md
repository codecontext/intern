# Intern Agent Architecture

## 1. Purpose

An agent extends Intern from answering questions to performing controlled multi-step tasks.

---

# 2. Evolution

```text
LLM

Question
 ↓
Answer
```

```text
RAG

Question
 ↓
Retrieve
 ↓
Answer
```

```text
Agent

Goal
 ↓
Decide
 ↓
Tool
 ↓
Observe
 ↓
Decide
 ↓
Tool
 ↓
...
 ↓
Result
```

---

# 3. Agent Responsibilities

The agent orchestrator coordinates:

* Goal
* Available context
* Tools
* Observations
* Task state
* Permissions
* Final response

---

# 4. Agent Loop

Conceptually:

```text
Receive Goal
     ↓
Understand Task
     ↓
Select Action
     ↓
Execute Tool
     ↓
Observe Result
     ↓
Determine Next Action
     ↓
Repeat or Finish
```

---

# 5. Tool Selection

Tools should be explicitly registered.

Example:

```text
read_file
search_code
search_symbol
run_tests
search_web
```

The agent should only be able to use tools that are available and permitted.

---

# 6. Agent State

Potential state:

```text
goal
conversation_id
knowledge_base_id
available_tools
observations
actions
permissions
status
result
```

---

# 7. Read-Only First

The initial agent should prioritize read-only operations.

Examples:

```text
Search repository
Read files
Search documentation
Inspect configuration
Analyze logs
```

Modification and execution capabilities should be introduced later.

---

# 8. Termination

An agent must have explicit termination conditions.

Examples:

```text
Task completed
Insufficient information
Maximum iterations reached
Tool failure
Permission denied
User cancelled
```

---

# 9. Observability

The UI should show observable activity:

```text
✓ Searched repository
✓ Found I2C implementation
✓ Read DMA implementation
✓ Compared UART implementation
✓ Generated analysis
```

Private chain-of-thought should not be exposed.

---

# 10. Agent vs Application Logic

The agent should not replace normal application services.

For example:

```text
Conversation Service
```

should remain responsible for conversation operations.

The agent orchestrates those capabilities when necessary.

---

# 11. Future

Potential capabilities:

* Planning
* Multi-step debugging
* Test investigation
* Build/test loops
* Git analysis
* Implementation planning
* Controlled code modification
