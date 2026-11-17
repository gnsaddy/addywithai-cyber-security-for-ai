# app_basics.py: security basics for ShopBot. Stdlib only, no API key needed.
import os, re, secrets

# 1) Secrets come from the environment, never from the code or git
API_KEY = os.environ.get("SHOPBOT_API_KEY")
if not API_KEY:
    raise SystemExit("Stopped: SHOPBOT_API_KEY is not set (put it in .env).")
print("Key loaded:", API_KEY[:4] + "****")  # never print or log the full key

# 2) Least privilege: each role gets only what it needs
ROLES = {"asha": "customer", "ravi": "support", "meena": "admin"}
PERMS = {
    "customer": {"view_own_order"},
    "support": {"view_own_order", "view_any_order"},
    "admin": {"view_own_order", "view_any_order", "refund"},
}
SESSIONS = {}  # session token -> user name

def login(user):  # authentication: who are you?
    token = secrets.token_urlsafe(16)  # long, random, unguessable
    SESSIONS[token] = user
    return token

def can(token, action):  # authorization: what may you do?
    user = SESSIONS.get(token)
    if user is None:
        return False  # not logged in: deny
    return action in PERMS.get(ROLES[user], set())  # deny by default

# 3) Input validation: check type, size and format before you use it
ORDER_ID = re.compile(r"ORD-\d{6}")

def clean_message(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("empty message")
    if len(text) > 2000:
        raise ValueError("too long (max 2000 chars)")  # also caps the LLM bill
    return text.strip()

def check_order_id(order_id):
    if not ORDER_ID.fullmatch(order_id):
        raise ValueError(f"bad order id {order_id!r}")
    return order_id

# 4) Try it
asha, meena = login("asha"), login("meena")
TESTS = [("asha", asha, "view_own_order"), ("asha", asha, "refund"),
         ("meena", meena, "refund"), ("nobody", "made-up", "view_own_order")]
for who, token, action in TESTS:
    print(f"{who:7} {action:15}", "ALLOW" if can(token, action) else "DENY")

INPUTS = [(clean_message, "  Where is my order?  "), (clean_message, "x" * 5000),
          (check_order_id, "ORD-123456"), (check_order_id, "ORD-12AB")]
for check, value in INPUTS:
    try:
        print("OK     ", repr(check(value))[:40])
    except ValueError as e:
        print("REJECT ", e)
