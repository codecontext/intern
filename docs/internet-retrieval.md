# Intern Internet Retrieval

## 1. Purpose

Internet retrieval provides information unavailable in the local LLM and project knowledge base.

It is an optional context source.

---

# 2. Architecture

```text
User Question
      ↓
Application
      ↓
Search Provider
      ↓
Search Results
      ↓
Content Retrieval
      ↓
Relevant Information
      ↓
LLM
```

---

# 3. Explicit Control

Internet access should be explicitly enabled.

```text
Internet: ON
```

must have different behaviour from:

```text
Internet: OFF
```

When disabled, Intern should not perform external searches.

---

# 4. Source Separation

Internet information should remain distinguishable from internal information.

```text
Internal Project Evidence
        ≠
Internet Evidence
```

---

# 5. Source Attribution

External answers should preserve:

```text
Source title
URL
Retrieved information
```

The final UI should make external sources inspectable.

---

# 6. Conflicting Information

When internal and external information differ, Intern should present the distinction rather than silently replacing one with the other.

Example:

```text
Internal project documentation states X.

External documentation states Y.

The two sources differ because...
```

---

# 7. Security

Internet retrieval introduces potential risks:

* Data leakage through search queries
* Malicious web content
* Prompt injection
* Untrusted instructions
* External content attempting to influence tools

Retrieved web content must be treated as untrusted data.

---

# 8. Future Controls

Potential controls:

```text
Allowed domains
Blocked domains
Search provider
Maximum results
Timeout
External content limits
```
