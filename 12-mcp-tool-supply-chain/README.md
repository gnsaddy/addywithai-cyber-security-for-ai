# Lecture 12, MCP and Tool Supply-Chain Risks: demo code

An auditor for MCP-style tool definitions: run it before you install or update tools.
Plain Python 3, standard library only. `tools.json` holds three fake tool definitions; the poisoned one uses a harmless `TEST-POISON` marker, not a working attack.

| Part of `audit_tools.py` | What it shows |
|---|---|
| `RED_FLAGS` | phrases that never belong in a tool description ("do not tell", "before using any tool", private files...) |
| `BROAD` | scopes that are too powerful (`files:*`, `repo:admin`, ...) |
| `TRUSTED_NAMES` | which server we trust for a tool name (catches shadowing) |
| `fingerprint()`, `check_pins()` | a hash of each definition saved at approval; any later change = review again (rug pull check) |

## Run
```
python audit_tools.py
```

Output (tested 2026-11-17, Python 3):
```
OK     weather-mcp/get_forecast []
REVIEW notes-helper/add_note ['suspicious description', 'broad scope files:*', 'version not pinned']
REVIEW gh-tools/send_email ['broad scope repo:admin', 'name shadows a trusted tool']
CHANGED SINCE APPROVAL: ['get_forecast']
```

## What to take away
* Read the source, pin versions AND tool definitions, read every description, use an approved list.
* Give each server narrow scopes and its own short-lived token; no token passthrough.
* Run servers in a container with a network allow-list; approve writes; log every call.
* Defensive use only. Test only systems you own or have permission to test.
