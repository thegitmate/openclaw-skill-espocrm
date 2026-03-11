#!/usr/bin/env python3
"""
EspoCRM Opportunity operations.

Usage:
  python3 -m scripts.opportunity list [--limit 20] [--offset 0] [--where FIELD VALUE]...
  python3 -m scripts.opportunity get <id>
  python3 -m scripts.opportunity search --FIELD VALUE
  python3 -m scripts.opportunity create --name "Deal name" --accountName "Acme" --closeDate "2025-12-31" [--FIELD VALUE]...
  python3 -m scripts.opportunity update <id> --FIELD VALUE [--FIELD VALUE]...
  python3 -m scripts.opportunity delete <id>
"""

import sys
import requests
from . import get_config, headers, success, error, parse_response, clean_payload

ENTITY = "Opportunity"
SUMMARY_FIELDS = ["id", "name", "accountName", "stage", "amount", "probability", "closeDate", "assignedUserName", "leadSource"]

def list_records(args):
    api_url, api_key, cf_id, cf_secret = get_config()
    limit = 20
    offset = 0
    where_filters = []

    i = 0
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i+1]); i += 2
        elif args[i] == "--offset" and i + 1 < len(args):
            offset = int(args[i+1]); i += 2
        elif args[i] == "--where" and i + 2 < len(args):
            where_filters.append((args[i+1], args[i+2])); i += 3
        else:
            i += 1

    params = {"maxSize": limit, "offset": offset}
    for idx, (field, value) in enumerate(where_filters):
        params[f"where[{idx}][type]"] = "equals"
        params[f"where[{idx}][attribute]"] = field
        params[f"where[{idx}][value]"] = value

    r = requests.get(f"{api_url}/{ENTITY}", headers=headers(api_key, cf_id, cf_secret), params=params, timeout=10)
    data = parse_response(r)
    records = data.get("list", [])
    success([{f: rec.get(f) for f in SUMMARY_FIELDS} for rec in records])

def get_record(args):
    if not args:
        error("Missing opportunity ID")
    api_url, api_key, cf_id, cf_secret = get_config()
    r = requests.get(f"{api_url}/{ENTITY}/{args[0]}", headers=headers(api_key, cf_id, cf_secret), timeout=10)
    success(parse_response(r))

def search_records(args):
    if len(args) < 2:
        error("Usage: search --FIELD VALUE")
    api_url, api_key, cf_id, cf_secret = get_config()
    field = args[0].lstrip("-")
    value = args[1]
    params = {"where[0][type]": "equals", "where[0][attribute]": field, "where[0][value]": value}
    r = requests.get(f"{api_url}/{ENTITY}", headers=headers(api_key, cf_id, cf_secret), params=params, timeout=10)
    data = parse_response(r)
    records = data.get("list", [])
    success([{f: rec.get(f) for f in SUMMARY_FIELDS} for rec in records])

def create_record(args):
    payload = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            payload[args[i].lstrip("-")] = args[i+1]; i += 2
        else:
            i += 1
    if not payload:
        error("No fields provided. Use --name 'Deal' --accountName 'Acme' --closeDate '2025-12-31'")
    api_url, api_key, cf_id, cf_secret = get_config()
    r = requests.post(f"{api_url}/{ENTITY}", json=payload, headers=headers(api_key, cf_id, cf_secret), timeout=10)
    success(parse_response(r))

def update_record(args):
    if not args:
        error("Missing opportunity ID. Usage: update <id> --field value")
    record_id = args[0]
    payload = {}
    i = 1
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            payload[args[i].lstrip("-")] = args[i+1]; i += 2
        else:
            i += 1
    if not payload:
        error("No fields provided.")
    api_url, api_key, cf_id, cf_secret = get_config()
    payload = clean_payload(payload)
    r = requests.put(f"{api_url}/{ENTITY}/{record_id}", json=payload, headers=headers(api_key, cf_id, cf_secret), timeout=10)
    success(parse_response(r))

def delete_record(args):
    if not args:
        error("Missing opportunity ID. Usage: delete <id>")
    record_id = args[0]
    api_url, api_key, cf_id, cf_secret = get_config()
    r = requests.delete(f"{api_url}/{ENTITY}/{record_id}", headers=headers(api_key, cf_id, cf_secret), timeout=10)
    success(parse_response(r))

def link_record(args):
    if len(args) < 3:
        error("Usage: link <id> <relation> <related_id>")
    record_id = args[0]
    relation = args[1]
    related_id = args[2]
    api_url, api_key, cf_id, cf_secret = get_config()
    payload = {"id": related_id}
    r = requests.post(f"{api_url}/{ENTITY}/{record_id}/{relation}", json=payload, headers=headers(api_key, cf_id, cf_secret), timeout=10)
    success(parse_response(r))

def describe(args):
    api_url, api_key, cf_id, cf_secret = get_config()
    r = requests.get(f"{api_url}/Metadata", headers=headers(api_key, cf_id, cf_secret), timeout=10)
    data = parse_response(r)
    entity_fields = data.get("entityDefs", {}).get(ENTITY, {}).get("fields", {})
    if not entity_fields:
        error(f"No metadata found for entity: {ENTITY}")
    result = {}
    for field_name, field_def in entity_fields.items():
        field_type = field_def.get("type")
        entry = {"type": field_type}
        if "options" in field_def:
            entry["options"] = field_def["options"]
        if field_def.get("required"):
            entry["required"] = True
        result[field_name] = entry
    success(result)

def create_record(args):
    payload = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            payload[args[i].lstrip("-")] = args[i+1]; i += 2
        else:
            i += 1
    if not payload:
        error("No fields provided. Use --name 'Acme Corp'")
    api_url, api_key, cf_id, cf_secret = get_config()
    payload = clean_payload(payload)
    r = requests.post(f"{api_url}/{ENTITY}", json=payload, headers=headers(api_key, cf_id, cf_secret), timeout=10)
    data = parse_response(r)
    # Check which sent fields are missing or null in the response
    ignored = [k for k, v in payload.items() if data.get(k) is None]
    response = {"id": data.get("id"), "created": data.get("name") or data.get("id")}
    if ignored:
        response["warning"] = f"These fields were sent but came back null (may be invalid field names): {', '.join(ignored)}"
    success(response)

def get_links(args):
    if len(args) < 2:
        error("Usage: get-links <id> <relation>")
    record_id = args[0]
    relation = args[1]
    api_url, api_key, cf_id, cf_secret = get_config()
    params = {}
    if len(args) > 2 and args[2] == "--limit":
        params["maxSize"] = args[3]
    r = requests.get(f"{api_url}/{ENTITY}/{record_id}/{relation}", headers=headers(api_key, cf_id, cf_secret), params=params, timeout=10)
    data = parse_response(r)
    records = data.get("list", data)
    success(records)

def list_relationships(args):
    api_url, api_key, cf_id, cf_secret = get_config()
    r = requests.get(f"{api_url}/Metadata", headers=headers(api_key, cf_id, cf_secret), timeout=10)
    data = parse_response(r)
    links = data.get("entityDefs", {}).get(ENTITY, {}).get("links", {})
    if not links:
        error(f"No relationships found for entity: {ENTITY}")
    result = {}
    for link_name, link_def in links.items():
        result[link_name] = {
            "type": link_def.get("type"),
            "entity": link_def.get("entity")
        }
    success(result)

def main():
    args = sys.argv[1:]
    if not args:
        error("Missing command: list | get | search | create | update | delete | link | get-links | list-relationships | describe")
    cmd = args[0]
    rest = args[1:]
    try:
        if cmd == "list":     list_records(rest)
        elif cmd == "get":    get_record(rest)
        elif cmd == "search": search_records(rest)
        elif cmd == "create": create_record(rest)
        elif cmd == "update": update_record(rest)
        elif cmd == "delete": delete_record(rest)
        elif cmd == "link":   link_record(rest)
        elif cmd == "describe": describe(rest)
        elif cmd == "get-links":          get_links(rest)
        elif cmd == "list-relationships": list_relationships(rest)
        else: error(f"Unknown command: {cmd}")
    except requests.RequestException as e:
        error(str(e))

if __name__ == "__main__":
    main()