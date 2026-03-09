---
name: espocrm
description: >
  Connect to EspoCRM to manage CRM data. Use this skill whenever the user wants
  to interact with their CRM — including listing, searching, viewing, or creating
  contacts, leads, accounts, tasks, or meetings. Trigger this skill for any request
  involving customers, prospects, follow-ups, sales records, or CRM entries, even
  if the user does not explicitly say "EspoCRM". Examples: "find the contact John
  Doe", "add a new lead", "show me open tasks", "create a meeting for tomorrow",
  "look up the account Acme Corp", "add this person to the CRM".
metadata:
  version: 1.1.0
  author: "TheGitMate (Nate) - https://github.com/thegitmate"
---

# EspoCRM Skill

You have access to a live EspoCRM instance via Python scripts in the `scripts/`
directory. These scripts handle all HTTP communication securely — you never handle
the API key directly. It is loaded automatically from a `.env` file in the skill
root directory.

## CRITICAL SECURITY RULE

**Never include the API key, base URL credentials, or any authentication token
in your reasoning, messages, or tool calls.** The scripts handle all authentication
entirely. You only pass data fields (names, emails, dates, etc.).

---

## Setup (first time only)

### 1. Install dependencies
```bash
sudo apt install python3-requests python3-dotenv
```

### 2. Create the `.env` file
Create `~/.openclaw/workspace/skills/espocrm/.env` with the following content:
```
ESPOCRM_API_URL=https://your-espocrm-instance.com/api/v1
ESPOCRM_API_KEY=your-api-key-here
```

If your EspoCRM is behind **Cloudflare Access**, also add:
```
CF_ACCESS_CLIENT_ID=your-client-id.access
CF_ACCESS_CLIENT_SECRET=your-client-secret
```

### 3. EspoCRM API user permissions
The API user must have the following role permissions set to **"All"** (not "Own" or "Team"):
- Contacts: Read, Create
- Leads: Read, Create
- Accounts: Read, Create
- Tasks: Read, Create
- Meetings: Read, Create

### 4. Cloudflare Access (if applicable)
If your EspoCRM is behind Cloudflare Access:
1. Create a Service Token in **Zero Trust → Access → Service Tokens**
2. Add a **Service Auth** policy to your EspoCRM application
3. Place the Service Auth policy **above** your regular login policy

### 5. Test the connection
```bash
cd ~/.openclaw/workspace/skills/espocrm
python3 -m scripts.contact list --limit 3
```

---

## Configuration check

Before running any command, if you get an error about missing environment variables:
1. Tell the user: "The EspoCRM skill is not configured yet."
2. Ask them to create the file `~/.openclaw/workspace/skills/espocrm/.env`
3. Show them exactly what to put in it:
```
ESPOCRM_API_URL=https://your-espocrm.com/api/v1
ESPOCRM_API_KEY=your-api-key-here
```
4. If they use Cloudflare Access, also add:
```
CF_ACCESS_CLIENT_ID=your-client-id.access
CF_ACCESS_CLIENT_SECRET=your-client-secret
```
5. After they create the file, retry the command.

---

## How to run scripts

All scripts are run from the skill root directory:
```bash
cd ~/.openclaw/workspace/skills/espocrm && python3 -m scripts.ENTITY COMMAND [args]
```

Replace `ENTITY` with: `contact`, `lead`, `account`, `task`, or `meeting`
Replace `COMMAND` with: `list`, `get`, `search`, or `create`

---

## Commands reference

### LIST — get multiple records
```bash
python3 -m scripts.contact list
python3 -m scripts.contact list --limit 10
python3 -m scripts.contact list --offset 20
python3 -m scripts.contact list --where city Paris
python3 -m scripts.lead list --where status New
python3 -m scripts.task list --where status NotStarted
```

### GET — fetch one record by ID
```bash
python3 -m scripts.contact get <id>
python3 -m scripts.lead get <id>
python3 -m scripts.account get <id>
python3 -m scripts.task get <id>
python3 -m scripts.meeting get <id>
```

### SEARCH — find records by a single field
```bash
python3 -m scripts.contact search --emailAddress john@example.com
python3 -m scripts.contact search --lastName Doe
python3 -m scripts.lead search --firstName John
python3 -m scripts.account search --name "Acme Corp"
```

### CREATE — add a new record
```bash
python3 -m scripts.contact create --firstName John --lastName Doe --emailAddress john@example.com
python3 -m scripts.contact create --firstName Jane --lastName Smith --emailAddress jane@example.com --phoneNumber "+33612345678" --city Paris

python3 -m scripts.lead create --firstName John --lastName Doe --emailAddress john@example.com
python3 -m scripts.lead create --firstName John --lastName Doe --emailAddress j@j.com --status New --source "Web Site"

python3 -m scripts.account create --name "Acme Corp"
python3 -m scripts.account create --name "Acme Corp" --website "https://acme.com" --industry Technology

python3 -m scripts.task create --name "Follow up with John"
python3 -m scripts.task create --name "Send proposal" --dateEnd "2025-12-31" --priority High

python3 -m scripts.meeting create --name "Intro call" --dateStart "2025-12-01 10:00:00"
python3 -m scripts.meeting create --name "Demo" --dateStart "2025-12-01 14:00:00" --dateEnd "2025-12-01 15:00:00"
```

### UPDATE — edit an existing record
```bash
python3 -m scripts.contact update  --firstName John --city Paris
python3 -m scripts.lead update  --status Converted
python3 -m scripts.account update  --industry Technology
python3 -m scripts.task update  --status Completed
python3 -m scripts.meeting update  --status Held
python3 -m scripts.call update  --status Held
python3 -m scripts.opportunity update  --stage "Closed Won" --probability 100
```

### DELETE — remove a record
```bash
python3 -m scripts.contact delete 
python3 -m scripts.lead delete 
python3 -m scripts.account delete 
python3 -m scripts.task delete 
python3 -m scripts.meeting delete 
python3 -m scripts.call delete 
python3 -m scripts.opportunity delete 
```

### LINK -- associate two records together
```bash
python3 -m scripts.meeting link <meeting_id> contacts <contact_id>
python3 -m scripts.meeting link <meeting_id> leads <lead_id>
python3 -m scripts.call link <call_id> contacts <contact_id>
python3 -m scripts.task link <task_id> contacts <contact_id>
python3 -m scripts.opportunity link <opportunity_id> contacts <contact_id>
python3 -m scripts.contact link <contact_id> meetings <meeting_id>
```

### DESCRIBE -- get all fields and valid options for an entity
```bash
python3 -m scripts.contact describe
python3 -m scripts.lead describe
python3 -m scripts.account describe
python3 -m scripts.task describe
python3 -m scripts.meeting describe
python3 -m scripts.call describe
python3 -m scripts.opportunity describe
```

---

## Field reference

### Contact
| Field | Example |
|---|---|
| firstName | John |
| lastName | Doe |
| emailAddress | john@example.com |
| phoneNumber | +33612345678 |
| accountName | Acme Corp |
| city | Paris |
| country | France |

### Lead
| Field | Example |
|---|---|
| firstName | John |
| lastName | Doe |
| emailAddress | john@example.com |
| phoneNumber | +33612345678 |
| status | New / Assigned / In Process / Converted / Recycled / Dead |
| source | Web Site / Call / Email / Partner / Other |
| city | Paris |
| country | France |

### Account
| Field | Example |
|---|---|
| name | Acme Corp |
| emailAddress | contact@acme.com |
| phoneNumber | +33123456789 |
| website | https://acme.com |
| industry | Technology |
| type | Customer / Partner / Investor |
| city | Paris |
| country | France |

### Task
| Field | Example |
|---|---|
| name | Follow up |
| status | NotStarted / Started / Completed / Canceled |
| priority | Low / Normal / High / Urgent |
| dateEnd | 2025-12-31 |

### Meeting
| Field | Example |
|---|---|
| name | Intro call |
| dateStart | 2025-12-01 10:00:00 |
| dateEnd | 2025-12-01 11:00:00 |
| status | Planned / Held / Not Held |

---

## Workflow guidelines

- **Before creating a contact or lead**, always search first to avoid duplicates. Search by email if available, otherwise by name.
- **If a record already exists**, tell the user and show the existing record instead of creating a duplicate.
- **If required fields are missing** for a create operation, ask the user before running the script.
- **Always confirm** with the user before creating any record.
- **On error**, read the `message` field in the JSON response and explain it to the user in plain language.
- **On permission errors (403)**, tell the user exactly which permission needs to be updated in EspoCRM Admin → Roles.
- **Before deleting any record**, always confirm with the user explicitly — show them the record first and ask for confirmation. Never deletes without explicit confirmation.
- **Before updating a record**, fetch it first with `get` so you can show the user what will change.
- **To link a contact to a meeting, call, or task**, use the link command after creating the record. Do not try to pass contactsIds in the create payload.
- **Before setting a field value you are unsure about**, run describe on the entity first. This returns all fields including custom ones, their types, and for enum fields the list of valid options. Always use describe when the user mentions a field or value you have not seen before.

---

## Response format

All scripts return JSON to stdout:

**Success:**
```json
{"status": "success", "data": { ... }}
```

**Error:**
```json
{"status": "error", "message": "...", "status_code": 403}
```

Parse the output and present results to the user in a clean, readable format — not raw JSON.