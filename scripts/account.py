#!/usr/bin/env python3
"""
EspoCRM Account operations.

Usage:
  python -m scripts.account list [--limit 20] [--offset 0] [--where FIELD VALUE]...
  python -m scripts.account get <id>
  python -m scripts.account search --FIELD VALUE
  python -m scripts.account create --name "Acme Corp" [--FIELD VALUE]...
"""

import sys
import requests
from . import get_config, headers, success, error, parse_response

ENTITY = "Account"
SUMMARY_FIELDS = ["id", "name", "emailAddress", "phoneNumber", "website", "industry", "type", "city", "country"]

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
        error("Missing account ID")
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
        error("No fields provided. Use --name 'Acme Corp'")
    api_url, api_key, cf_id, cf_secret = get_config()
    r = requests.post(f"{api_url}/{ENTITY}", json=payload, headers=headers(api_key, cf_id, cf_secret), timeout=10)
    success(parse_response(r))

def update_record(args):
    if not args:
        error("Missing account ID. Usage: update <id> --field value")
    record_id = args[0]
    payload = {}
    i = 1
    while i < len(args):
        if args[i].startswith("--") and i + 1 < len(args):
            payload[args[i].lstrip("-")] = args[i+1]; i += 2
        else:
            i += 1
    if not payload:
        error("No fields provided. Use --firstName John --lastName Doe etc.")
    api_url, api_key, cf_id, cf_secret = get_config()
    r = requests.put(f"{api_url}/{ENTITY}/{record_id}", json=payload, headers=headers(api_key, cf_id, cf_secret), timeout=10)
    success(parse_response(r))

def delete_record(args):
    if not args:
        error("Missing account ID. Usage: delete <id>")
    record_id = args[0]
    api_url, api_key, cf_id, cf_secret = get_config()
    r = requests.delete(f"{api_url}/{ENTITY}/{record_id}", headers=headers(api_key, cf_id, cf_secret), timeout=10)
    success(parse_response(r))

def main():
    args = sys.argv[1:]
    if not args:
        error("Missing command: list | get | search | create | update | delete")
    cmd = args[0]
    rest = args[1:]
    try:
        if cmd == "list":     list_records(rest)
        elif cmd == "get":    get_record(rest)
        elif cmd == "search": search_records(rest)
        elif cmd == "create": create_record(rest)
        elif cmd == "update": update_record(rest)
        elif cmd == "delete": delete_record(rest)
        else: error(f"Unknown command: {cmd}")
    except requests.RequestException as e:
        error(str(e))

if __name__ == "__main__":
    main()