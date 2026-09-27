# Intern Security

## 1. Purpose

Intern may eventually process source code, architecture documents, proprietary specifications, logs, and other sensitive engineering information.

Security must therefore be considered as the system evolves.

---

# 2. Local-First Security

The preferred architecture keeps project information local:

```text
Project Data
   ↓
Local Ingestion
   ↓
Local Embeddings
   ↓
Local Vector Store
   ↓
Local LLM
```

External transmission should be explicit.

---

# 3. Data Boundaries

Intern should distinguish:

```text
Local Project Data
Conversation Data
Knowledge Base Data
Internet Data
Tool Data
Audit Data
```

---

# 4. Secrets

Never commit:

```text
API keys
Passwords
Tokens
Private certificates
Credentials
```

Use environment configuration or an appropriate secret-management mechanism.

---

# 5. Web Retrieval Security

Internet content is untrusted.

Web pages may contain:

* Incorrect information
* Malicious instructions
* Prompt injection
* Embedded commands
* Misleading content

Retrieved web content must be treated as data, not as trusted system instructions.

---

# 6. Tool Security

Tools represent a security boundary.

Particularly sensitive:

```text
write_file
delete_file
execute_command
run_build
git operations
```

Tool availability must not automatically imply authorization.

---

# 7. Authentication

Authentication may not be required for a single-user local deployment.

It becomes important when Intern is exposed to multiple users.

Potential future mechanisms:

```text
Internal SSO
OIDC
LDAP/Active Directory
```

The actual mechanism should be selected based on organizational requirements.

---

# 8. Authorization

Future multi-user deployments should control:

```text
User → Knowledge Base
User → Conversation
User → Tool
User → Project
```

A user should not automatically have access to another user's knowledge.

---

# 9. Data Isolation

Knowledge retrieval must respect ownership and authorization boundaries.

Conceptually:

```text
User A
 └── Project A
      └── Knowledge A

User B
 └── Project B
      └── Knowledge B
```

Cross-project retrieval should require explicit authorization.

---

# 10. Auditability

Sensitive operations should eventually record:

```text
User
Timestamp
Action
Tool
Target
Permission decision
Result
```

---

# 11. Network Exposure

A local development server should not be exposed publicly without appropriate security controls.

Future internal deployment should consider:

```text
TLS
Authentication
Authorization
Firewall rules
Network segmentation
```

---

# 12. Security Principle

Intern should follow:

```text
Least privilege
+
Explicit permissions
+
Local-first data handling
+
Clear trust boundaries
+
Auditable consequential actions
```
