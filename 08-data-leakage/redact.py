# redact.py: mask personal data + secrets before you send or log text. Stdlib.
import re

PATTERNS = [  # order matters: keys and cards before phones
    ("KEY", r"\b(?:sk-[\w-]{16,}|AKIA[0-9A-Z]{16})\b"),
    ("CARD", r"\b(?:\d[ -]?){12,15}\d\b"),
    ("EMAIL", r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    ("PHONE", r"(?:\+91[ -]?)?\b[6-9]\d{9}\b"),
]

def redact(text):
    """Swap each match for a placeholder like <EMAIL_1>. Returns (text, vault)."""
    vault = {}
    for label, pattern in PATTERNS:
        def swap(m):
            n = sum(k.startswith("<" + label) for k in vault) + 1
            key = f"<{label}_{n}>"
            vault[key] = m.group()
            return key
        text = re.sub(pattern, swap, text)
    return text, vault

def restore(text, vault):  # put real values back, only inside our own app
    for key, value in vault.items():
        text = text.replace(key, value)
    return text

def minimize(order):  # send only the fields this task needs
    return {k: order[k] for k in ("item", "status")}

if __name__ == "__main__":
    msg = ("I'm Asha, asha.k@example.com, +91 9876543210. "
           "Card 4111 1111 1111 1111 was charged twice. "
           "Also my key sk-test-51abcDEF0123456789 stopped working.")
    clean, vault = redact(msg)
    print("SENT TO API:", clean)
    reply = "Sorry! We emailed <EMAIL_1> about the refund."  # stand-in model reply
    print("SHOWN TO USER:", restore(reply, vault))
    order = {"id": "ORD-123456", "item": "headphones", "status": "shipped",
             "address": "12 MG Road, Bengaluru", "phone": "9876543210"}
    print("ORDER SENT:", minimize(order))
