# threat_model.py: a tiny STRIDE threat model for ShopBot. Stdlib only.
# Describe the app as data, get a ranked threat list + a test checklist.

APP = {
    "name": "ShopBot",
    "flows": [  # (from, to, crosses a trust boundary?)
        ("customer", "chat API", True),
        ("help docs", "prompt", True),
        ("chat API", "LLM API", True),
        ("LLM", "order lookup", False),
        ("LLM", "refund tool", False),
    ],
    "tools": {"order lookup": "read", "refund tool": "write"},
    "logs_tool_calls": False,
}

def crosses(app, source):
    return any(f == source and b for f, _, b in app["flows"])

def has_tool(app, kind):
    return kind in app["tools"].values()

RULES = [  # (STRIDE, threat, applies?, likelihood 1-5, impact 1-5, test)
    ("E", "Chat text makes the bot call the refund tool",
     lambda a: has_tool(a, "write"), 4, 5,
     "Refunds over a limit need human approval"),
    ("I", "Bot shows another customer's order",
     lambda a: has_tool(a, "read"), 3, 5,
     "User A asks for user B's order: refused"),
    ("T", "Planted instructions in chat or help docs",
     lambda a: crosses(a, "customer") or crosses(a, "help docs"), 4, 4,
     "A harmless planted line is ignored"),
    ("D", "Long prompts and bots run up the bill",
     lambda a: crosses(a, "customer"), 4, 3,
     "Rate limit + daily cost cap kick in"),
    ("R", "No record of who triggered a refund",
     lambda a: not a["logs_tool_calls"], 3, 3,
     "Every tool call lands in the audit log"),
    ("S", "Text pretends to be the system or an admin",
     lambda a: crosses(a, "customer"), 2, 3,
     "Fake 'system' text never changes the role"),
]

threats = []
for letter, threat, applies, likely, impact, test in RULES:
    if applies(APP):
        threats.append((likely * impact, letter, threat, test))
threats.sort(key=lambda t: -t[0])  # highest risk first

print(f"Threat model: {APP['name']} ({len(threats)} threats)")
for score, letter, threat, _ in threats:
    print(f"{score:>3}  [{letter}] {threat}")
print("\nTest checklist (top 3):")
for score, _, _, test in threats[:3]:
    print(f"  [ ] {test}")
