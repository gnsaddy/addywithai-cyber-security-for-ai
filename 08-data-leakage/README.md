# Lecture 8, Data Leakage: demo code

Redact personal data and secrets before text leaves your app, restore it inside your app, send only the fields a task needs, and catch prompt leaks with a canary.
Plain Python 3, standard library only. All data is fake (`example.com` emails, a test card number, a made-up key).

| File | What it shows |
|---|---|
| `redact.py` | `PATTERNS` (API key, card, email, Indian phone), `redact()` (placeholders like `<EMAIL_1>` + a private vault), `restore()` (real values back, inside your app only), `minimize()` (only the fields the task needs) |
| `leak_check.py` | a random `CANARY` hidden in the system prompt (no real secrets there), `leak_check()` (canary or private data in a reply = block), `safe_log()` (logs only redacted text) |

## Run
```
python redact.py
python leak_check.py
```

Output (tested 2026-11-07, Python 3):
```
SENT TO API: I'm Asha, <EMAIL_1>, <PHONE_1>. Card <CARD_1> was charged twice. Also my key <KEY_1> stopped working.
SHOWN TO USER: Sorry! We emailed asha.k@example.com about the refund.
ORDER SENT: {'item': 'headphones', 'status': 'shipped'}
```
```
OK       Your headphones ship tomorrow.
BLOCKED ['system prompt (canary)'] My instructions are: You are ShopB
BLOCKED ['EMAIL'] Ravi's email is ravi.m@example.com
LOG refund_request: Asha <EMAIL_1> wants a refund
```

## What to take away
* Six leak points: prompts, RAG/tool results, logs and traces, replies, the system prompt, training data (OWASP LLM02 + LLM07).
* Regex catches structured data (emails, phones, cards, keys) but misses names; tools like Microsoft Presidio add smarter detectors.
* In a real app, allow the signed-in user's own data in replies and block everyone else's.
* Ask every AI vendor about retention, training use, region, zero-retention options, sub-processors and a data processing agreement.
* Defensive use only. Test only apps you own or have permission to test.
