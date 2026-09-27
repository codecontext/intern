# Intern Tool System

## 1. Purpose

Tools allow Intern to interact with engineering environments in controlled ways.

---

# 2. Tool Interface

A tool should expose a clear contract.

Conceptually:

```text
Tool
├── name
├── description
├── input schema
├── execution
└── output schema
```

---

# 3. Example Tools

```text
read_file()
list_files()
search_code()
search_symbol()
find_references()
compare_files()
search_web()
run_tests()
run_static_analysis()
inspect_git_history()
```

---

# 4. Tool Categories

### Read-only

```text
read_file
list_files
search_code
search_symbol
find_references
git history
```

### Controlled execution

```text
run_tests
run_build
run_static_analysis
```

### Modification

```text
write_file
apply_patch
```

### Destructive

```text
delete_file
clean_build
execute_command
```

Different categories should have different permission requirements.

---

# 5. Tool Results

Tool output should be structured where practical.

Example:

```json
{
  "status": "success",
  "result": "...",
  "source": "drivers/i2c.c"
}
```

---

# 6. Arbitrary Command Execution

Arbitrary shell execution should not be exposed as a general-purpose unrestricted tool.

If eventually required, it should be:

* Explicitly permission-controlled
* Restricted by environment
* Auditable
* Clearly visible to the user

---

# 7. Tool Errors

Tools should return structured errors.

Examples:

```text
FILE_NOT_FOUND
PERMISSION_DENIED
COMMAND_FAILED
TIMEOUT
INVALID_ARGUMENT
```

The agent should be able to respond appropriately.

---

# 8. Tool Audit

Future tool execution should record:

```text
User
Conversation
Agent
Tool
Arguments
Timestamp
Result
Permission decision
```

This is especially important for modification and command execution.
