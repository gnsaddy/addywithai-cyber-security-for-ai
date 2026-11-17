# safe_agent.py: agent loop with tiers, approval, budgets, audit log. Stdlib.
import json, time
from pathlib import Path

WORKSPACE = Path("workspace").resolve()  # the only folder file tools may touch

def read_file(name):
    path = (WORKSPACE / name).resolve()
    if not path.is_relative_to(WORKSPACE):  # sandbox: no ../ escapes
        raise PermissionError("outside workspace")
    return path.read_text()

def send_email(to, body):
    return f"(demo) email queued to {to}"

TOOLS = {  # name: (function, tier)
    "read_file": (read_file, "auto"),       # safe, read only
    "send_email": (send_email, "approve"),  # a human must say yes
    "delete_db": (None, "never"),           # not exposed at all
}
MAX_STEPS, MAX_COST = 5, 0.50  # budgets: steps and dollars per task

def audit(step, tool, args, result):
    line = {"t": round(time.time()), "step": step, "tool": tool,
            "args": args, "result": result}
    with open("audit.jsonl", "a") as f:  # append-only trail of every tool call
        f.write(json.dumps(line) + "\n")
    print(f"step {step} {tool:<10} -> {result}")

def run_tool(step, tool, args, approve):
    if tool not in TOOLS or TOOLS[tool][1] == "never":
        result = "BLOCKED: tool not allowed"
    elif TOOLS[tool][1] == "approve" and not approve(tool, args):
        result = "DENIED by human"
    else:
        try:
            result = TOOLS[tool][0](**args)
        except Exception as e:
            result = f"ERROR: {e}"
    audit(step, tool, args, result)
    return result

def run_agent(plan, approve, cost_per_step=0.12):
    spent = 0.0
    for step, (tool, args) in enumerate(plan, 1):  # stand-in model's calls
        if step > MAX_STEPS or spent + cost_per_step > MAX_COST:
            print(f"STOP at step {step}: budget reached (${spent:.2f} spent)")
            break
        spent += cost_per_step
        run_tool(step, tool, args, approve)

if __name__ == "__main__":
    WORKSPACE.mkdir(exist_ok=True)
    (WORKSPACE / "notes.txt").write_text("Order 123 shipped.")
    plan = [("read_file", {"name": "notes.txt"}),
            ("read_file", {"name": "../.env"}),
            ("send_email", {"to": "all-customers", "body": "TEST"}),
            ("delete_db", {}),
            ("read_file", {"name": "notes.txt"}),
            ("read_file", {"name": "notes.txt"})]
    run_agent(plan, approve=lambda tool, args: False)  # demo: the human says no
