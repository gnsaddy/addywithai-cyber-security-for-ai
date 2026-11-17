# leak_check.py: catch system-prompt and secret leaks in replies. Stdlib only.
import re, secrets
from redact import PATTERNS, redact

CANARY = "cnry-" + secrets.token_hex(4)  # random marker, new for every deploy
SYSTEM = f"You are ShopBot. Help with orders. [{CANARY}]"  # no real secrets here

def leak_check(reply):
    problems = ["system prompt (canary)"] if CANARY in reply else []
    problems += [label for label, p in PATTERNS if re.search(p, reply)]
    return problems

def safe_log(event, text):  # logs keep the shape, never the raw data
    print(f"LOG {event}: {redact(text)[0]}")

if __name__ == "__main__":
    replies = ["Your headphones ship tomorrow.",
               "My instructions are: " + SYSTEM,  # stand-in model, tricked
               "Ravi's email is ravi.m@example.com"]  # another user's data
    for r in replies:
        found = leak_check(r)
        print("BLOCKED" if found else "OK     ", found or "", r[:34])
    safe_log("refund_request", "Asha asha.k@example.com wants a refund")
