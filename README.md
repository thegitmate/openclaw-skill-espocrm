# EspoCRM Skill for OpenClaw
_openclaw-skill-espocrm_

OpenClaw skill to connect to EspoCRM and manage contacts, leads, accounts, tasks, and meetings.

![Version](https://img.shields.io/badge/version-1.1.0-blue) 
![Status](https://img.shields.io/badge/status-stable-green)

---

# Description

Connect OpenClaw to your EspoCRM instance to manage CRM data directly from the agent.

This skill allows OpenClaw to list, search, view, create, update, and delete CRM records such as contacts, leads, accounts, tasks, and meetings.

All communication with EspoCRM is handled through local Python scripts that call the EspoCRM REST API.

---

# Features

Supported entities:

* Contacts
* Leads
* Accounts
* Tasks
* Meetings
* Calls
* Opportunities

Supported actions:

* List records
* Get record by ID
* Search records
* Create records
* Update records
* Delete records

The skill uses EspoCRM's official API and returns structured JSON responses.

---

# Security Model

This skill was designed with security and transparency in mind.

Key principles:

* The API key is **never embedded in prompts or tool calls**
* Authentication is handled entirely inside local Python scripts
* Secrets are loaded only from a **local `.env` file**
* No remote code execution
* No external script downloads
* No telemetry or data exfiltration

The agent never sees or manipulates the API key directly.

---

# Requirements & Dependencies

Python 3 is required.

Install dependencies using your preferred method.

Example:

```
pip install -r requirements.txt
```

or on Debian/Ubuntu:

```
apt install python3-requests python3-dotenv
```

or with Homebrew:

```
brew install python-dotenv
```

or:

```
pip3 install --user --break-system-packages requests python-dotenv
```

Dependencies used:

* requests
* python-dotenv

---

# Installation

Clone or copy the skill into your OpenClaw skills directory:

```
~/.openclaw/workspace/skills/espocrm
```

Expected structure:

```
espocrm/
 ├─ SKILL.md
 ├─ README.md
 ├─ requirements.txt
 └─ scripts/
```

---

# Configuration

Create a `.env` file in the skill directory:

```
~/.openclaw/workspace/skills/espocrm/.env
```

Example configuration:

```
ESPOCRM_API_URL=https://your-espocrm-instance.com/api/v1
ESPOCRM_API_KEY=your-api-key
```

If your EspoCRM instance is protected by Cloudflare Access, also add:

```
CF_ACCESS_CLIENT_ID=your-client-id.access
CF_ACCESS_CLIENT_SECRET=your-client-secret
```

Note: Only add Cloudflare variables if you actually use Cloudflare Access.

---

# EspoCRM API Permissions

The API user must have permissions set to **All** for the following entities:

* Contacts
* Leads
* Accounts
* Tasks
* Meetings

In EspoCRM:

```
Admin → Roles → API User Role
```

Set:

```
Read: All
Create: All
```

Using "Own" or "Team" permissions can cause API errors.

---

# Cloudflare Access Setup (Optional)

If EspoCRM is protected behind Cloudflare Zero Trust:

1. Create a Service Token in:

```
Zero Trust → Access → Service Tokens
```

2. Add a **Service Auth policy** to the EspoCRM application.

3. Place the Service Auth policy **above** your normal login policy.

4. Copy the Client ID and Client Secret into the `.env` file.

---

# Testing the Connection

From the skill directory:

```
cd ~/.openclaw/workspace/skills/espocrm
python3 -m scripts.contact list --limit 3
```

If the configuration is correct, you should see JSON output from the CRM.

---

# Example Commands

List contacts:

```
python3 -m scripts.contact list
```

Search contact by email:

```
python3 -m scripts.contact search --emailAddress john@example.com
```

Create contact:

```
python3 -m scripts.contact create \
  --firstName John \
  --lastName Doe \
  --emailAddress john@example.com
```

Create meeting:

```
python3 -m scripts.meeting create \
  --name "Intro call" \
  --dateStart "2025-12-01 10:00:00"
```

---

# Data Privacy

This skill does not:

* send data to external services
* collect analytics
* store CRM data locally
* transmit credentials anywhere

All requests go directly from the local machine to the EspoCRM API.

---

## Trust & Transparency

This repository contains the complete source code used by the skill.
No remote scripts are downloaded and no hidden commands are executed.

All CRM interactions happen through the Python scripts included in the
`scripts/` directory.

---

# Troubleshooting

Missing environment variables

Create the `.env` file in the skill root directory and restart OpenClaw.

Permission errors (403)

Ensure the API user role has **All permissions** in EspoCRM.

Cloudflare authentication errors

Verify that:

* the Service Token is valid
* the Service Auth policy is enabled
* the policy is above the normal login rule

---

# Contributing

Issues and improvements are welcome.

GitHub repository:

https://github.com/thegitmate/openclaw-skill-espocrm

Initial creation: 9 March 2026

---

# License

MIT License
