import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the skill root directory
load_dotenv(Path(__file__).parent.parent / ".env")

def get_config():
    api_url = os.getenv("ESPOCRM_API_URL")
    api_key = os.getenv("ESPOCRM_API_KEY")

    if not api_url:
        print(json.dumps({"status": "error", "message": (
            "ESPOCRM_API_URL is not set. "
            "Create a .env file at ~/.openclaw/workspace/skills/espocrm/.env with:\n"
            "ESPOCRM_API_URL=https://your-espocrm.com/api/v1\n"
            "ESPOCRM_API_KEY=your-api-key-here"
        )}))
        sys.exit(1)

    if not api_key:
        print(json.dumps({"status": "error", "message": (
            "ESPOCRM_API_KEY is not set. "
            "Create a .env file at ~/.openclaw/workspace/skills/espocrm/.env with:\n"
            "ESPOCRM_API_URL=https://your-espocrm.com/api/v1\n"
            "ESPOCRM_API_KEY=your-api-key-here"
        )}))
        sys.exit(1)

    cf_client_id = os.getenv("CF_ACCESS_CLIENT_ID")
    cf_client_secret = os.getenv("CF_ACCESS_CLIENT_SECRET")

    return api_url.rstrip("/"), api_key, cf_client_id, cf_client_secret

def headers(api_key, cf_client_id=None, cf_client_secret=None):
    h = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }
    if cf_client_id and cf_client_secret:
        h["CF-Access-Client-Id"] = cf_client_id
        h["CF-Access-Client-Secret"] = cf_client_secret
    return h

def success(data):
    print(json.dumps({"status": "success", "data": data}))

def error(message, status_code=None):
    out = {"status": "error", "message": message}
    if status_code:
        out["status_code"] = status_code
    print(json.dumps(out))
    sys.exit(1)

def parse_response(r):
    is_json = r.headers.get("Content-Type", "").startswith("application/json")
    
    if r.status_code in (200, 201):
        return r.json() if is_json else {"raw": r.text}
    
    # Check for EspoCRM/Cloudflare specific error reasons
    status_reason = r.headers.get("x-status-reason", "")
    
    if r.status_code == 403:
        if "No read access" in status_reason:
            error("Permission denied: the API user does not have Read access for this entity. Update the role in EspoCRM Admin → Roles.", status_code=403)
        elif "No create access" in status_reason:
            error("Permission denied: the API user does not have Create access for this entity. Update the role in EspoCRM Admin → Roles.", status_code=403)
        elif "No edit access" in status_reason:
            error("Permission denied: the API user does not have Edit access for this entity. Update the role in EspoCRM Admin → Roles.", status_code=403)
        else:
            error(f"Access denied by Cloudflare or EspoCRM. Reason: {status_reason or 'unknown'}. Check Cloudflare Access policies and EspoCRM role permissions.", status_code=403)
    
    elif r.status_code == 401:
        error("Authentication failed: check your ESPOCRM_API_KEY in the .env file.", status_code=401)
    
    elif r.status_code == 500:
        error("EspoCRM server error (500): the request was malformed or the server crashed. Check field names and values.", status_code=500)
    
    elif r.status_code == 404:
        error("Record not found (404): the requested entity or ID does not exist in EspoCRM.", status_code=404)
    
    else:
        msg = r.json() if is_json else r.text
        error(f"Unexpected error {r.status_code}: {msg}", status_code=r.status_code)