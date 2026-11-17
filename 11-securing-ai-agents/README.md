# Lecture 11, Securing AI Agents: demo code

An agent loop with permission tiers, a sandboxed file tool, human approval, a step limit, a spend cap and an append-only audit log.
Plain Python 3 (3.9+), standard library only. The "model" is a fixed plan of tool calls (a stand-in), so no API key is needed.

| Part of `safe_agent.py` | What it shows |
|---|---|
| `WORKSPACE` + `read_file()` | the only folder the file tool may touch; `../` escapes are refused |
| `TOOLS` | each tool's tier: `auto`, `approve` (a human must say yes) or `never` (not exposed) |
| `MAX_STEPS`, `MAX_COST` | budgets per task: 5 steps, $0.50 |
| `audit()` | one JSON line per tool call appended to `audit.jsonl` |
| `run_tool()`, `run_agent()` | the gatekeeper and the loop |

## Run
```
python safe_agent.py
```
It creates a `workspace/` folder and an `audit.jsonl` file next to the script.

Output (tested 2026-11-17, Python 3):
```
step 1 read_file  -> Order 123 shipped.
step 2 read_file  -> ERROR: outside workspace
step 3 send_email -> DENIED by human
step 4 delete_db  -> BLOCKED: tool not allowed
STOP at step 5: budget reached ($0.48 spent)
```

## What to take away
* Give agents an allow-list of narrow tools, the user's rights (never admin), and a sandbox.
* Approval requests must show the exact tool and arguments; a "no" is final.
* Cap steps, spend, scope and time, and log every call.
* Defensive use only. Test only apps you own or have permission to test.
