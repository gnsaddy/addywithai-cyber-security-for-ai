# Lecture 5, Prompt Injection: demo code

A toy email summarizer, hijacked by a **harmless planted test line**, then hardened with three layers, then tested with canary lines.
Plain Python 3, standard library only. The "model" is a stand-in function (no API key, no network) and the tools are fake (they only print). No real email is read or sent; `example.com` addresses are reserved for examples.

| File | What it shows |
|---|---|
| `injection_demo.py` | `naive()` glues rules + email into one string and runs any action; `hardened()` adds layer 1 (flag order-like lines), layer 2 (drop them + wrap the email in `<email>` tags marked as data) and layer 3 (allow-list the action per task, block + log the rest) |
| `canary_test.py` | runs three harmless canary lines through both apps and counts how often the forward tool did NOT run |

## Run
```
python injection_demo.py
python canary_test.py
```

Output (tested 2026-11-07, Python 3):
```
NAIVE, email 1:
  TOOL RAN: forward_all_emails(to='win@example.com') <- hijacked
HARDENED, email 1:
  flagged lines: [3]
  Summary: Asks: Can we move Friday's design review to 3 pm?
HARDENED, email 2 (sneakier):
  flagged lines: none
  BLOCKED: forward_all_emails is not allowed for summarize (logged)
```
```
Naive:    0/3 canaries stopped
Hardened: 3/3 canaries stopped
```

## What to take away
* Email 2 shows why one layer is not enough: the detector missed the new wording and the (stand-in) model was fooled, but the allow-list still blocked the action.
* Real LLMs are not this simple. Delimiters and filters lower the risk but do not remove it, so keep tools small, check every action before it runs, and ask a human before sending, deleting or paying.
* Add a canary every time you see new wording, and run `canary_test.py` (or your own version against your real pipeline) before each release.
* Defensive use only. Test only apps you own or have permission to test.
