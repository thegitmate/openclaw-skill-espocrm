# Security Policy

## Scope

This skill connects to a self-hosted EspoCRM instance via its REST API.
It requires only outbound HTTPS access to the configured EspoCRM instance.
No data is sent to any third party. No inbound connections are opened.

---

## Security Principles

This skill follows several core security principles:

- **Least privilege** – the EspoCRM API user should only have the permissions required for the intended workflow.
- **Local secret storage** – credentials are stored only in a local `.env` file and never embedded in prompts or code.
- **No external telemetry** – the skill does not send data to analytics or third-party services.
- **Explicit execution** – all operations are performed through visible Python scripts included in this repository.
- **No remote code execution** – the skill does not download or execute code from external sources.

---

## Threat Model

### Assets
- EspoCRM API key
- CRM data (contacts, leads, accounts, tasks, meetings, calls, opportunities)

### Trust Boundaries
- The AI agent (OpenClaw) runs locally on the user's machine
- The EspoCRM instance is remote, access-controlled by the user
- Cloudflare Access sits in front of EspoCRM (optional but recommended)

### Threats Mitigated

| Threat | Mitigation |
|---|---|
| API key exposure to LLM | Key is never passed as an argument or included in prompts. Loaded from .env at script runtime only. |
| API key in version control | .gitignore excludes .env and .venv from all commits |
| Unauthorized CRM access | EspoCRM role limits the API user to specific entities and actions only |
| Overprivileged API user | Skill recommends least-privilege role configuration (no delete by default) |
| Man-in-the-middle attack | All communication is over HTTPS only |
| Cloudflare bypass | Service token is passed via headers, not URL parameters |
| Prompt injection via CRM data | Scripts return structured JSON only — no free-text fields are executed |

### Threats Not Mitigated (user responsibility)
- Physical access to the machine running OpenClaw
- Compromise of the EspoCRM server itself
- Expiry or rotation of the API key (user must update .env manually)

---

## Credentials

This skill uses two types of credentials, both stored in `.env`:

| Variable | Purpose | Required |
|---|---|---|
| ESPOCRM_API_URL | Base URL of your EspoCRM instance | Yes |
| ESPOCRM_API_KEY | EspoCRM API key for authentication | Yes |
| CF_ACCESS_CLIENT_ID | Cloudflare Access service token ID | Only if behind Cloudflare Access |
| CF_ACCESS_CLIENT_SECRET | Cloudflare Access service token secret | Only if behind Cloudflare Access |

**The `.env` file is excluded from version control via `.gitignore` and should
never be committed, shared, or included in skill distributions.**

---

## Recommended EspoCRM Role Configuration

Follow the principle of least privilege. Only grant the permissions your
use case actually requires. Example minimal configuration:

| Entity | Read | Create | Edit | Delete |
|---|---|---|---|---|
| Contacts | All | Yes | Yes | No |
| Leads | All | Yes | Yes | No |
| Accounts | All | Yes | Yes | No |
| Tasks | All | Yes | Yes | No |
| Meetings | All | Yes | Yes | No |
| Calls | All | Yes | Yes | No |
| Opportunities | All | Yes | Yes | No |

Delete is disabled by default. Enable only if explicitly needed.

---

## Local Filesystem Access

The skill only reads the following local file:

~/.openclaw/workspace/skills/espocrm/.env

No other files are accessed or modified.

The skill does not scan the filesystem, access user documents, or read
system configuration files.

---

## Reporting a Vulnerability

If you discover a security issue in this skill, please report it responsibly.

Please include:
- description of the vulnerability
- steps to reproduce
- potential impact
- suggested mitigation (if known)

You can report issues by opening a private GitHub issue or contacting
the maintainer directly.

Please avoid public disclosure until the issue has been investigated.
```

---

```
### 1. Install dependencies
```bash
sudo apt install python3-requests python3-dotenv
```
```

Replace with:
```
### 1. Install dependencies

This skill requires only outbound HTTPS access to your configured EspoCRM
instance. No other network access is needed.

Install the required Python packages using your system package manager
(no elevated privileges needed if pip user install is available):

Option A -- Debian/Ubuntu (recommended):
```
apt install python3-requests python3-dotenv
```

Option B -- pip user install (no sudo):
```
pip install --user requests python-dotenv
```

Option C -- Homebrew Python:
```
pip3 install --user --break-system-packages requests python-dotenv
```
