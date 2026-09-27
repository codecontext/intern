# Intern Permissions

## 1. Purpose

Permissions control what Intern and its agents are allowed to do.

The system should distinguish information retrieval from consequential actions.

---

# 2. Risk Levels

| Operation         | Initial Policy    |
| ----------------- | ----------------- |
| Read file         | Automatic         |
| Search repository | Automatic         |
| Search KB         | Automatic         |
| Search Internet   | User-controlled   |
| Run tests         | Controlled        |
| Run build         | Controlled        |
| Modify file       | Explicit approval |
| Delete file       | Explicit approval |
| Arbitrary command | Explicit approval |

These are architectural guidelines and may evolve.

---

# 3. Human Approval

Example:

```text
Intern wants to modify:

src/drivers/i2c.c

Reason:
Apply the proposed DMA initialization fix.

[Allow] [Deny]
```

---

# 4. Command Approval

Example:

```text
Intern wants to execute:

pytest tests/i2c/test_dma.py

[Allow] [Deny]
```

The user should understand what will happen before approving.

---

# 5. Permission Scope

Future permissions may be scoped by:

```text
Tool
Directory
Command
Knowledge Base
Project
User
Session
```

---

# 6. Destructive Actions

Destructive operations should require explicit confirmation.

Examples:

```text
Delete file
Overwrite file
Reset repository
Remove generated data
Execute destructive command
```

---

# 7. Audit

Permission decisions should eventually be auditable.

Record:

```text
Action
User
Timestamp
Tool
Arguments
Decision
Result
```

---

# 8. Principle

The agent should never gain more authority merely because it is capable of using a tool.

Capability and authorization are separate concepts.

```text
Can perform action
        ≠
Allowed to perform action
```
