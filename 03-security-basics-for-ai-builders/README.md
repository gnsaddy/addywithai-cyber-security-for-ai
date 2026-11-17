# Lecture 3, Security Basics for AI Builders: demo code

Two small files for **ShopBot**, the toy online-shop chatbot of this playlist.
Plain Python 3, standard library only. No installs, no real API key, no network.

| File | What it shows |
|---|---|
| `app_basics.py` | secrets loaded from the environment (fails closed), least-privilege roles, `login()` = authentication, `can()` = authorization with deny by default, input validation with an allow-list |
| `secret_scan.py` | a git **pre-commit** secret scan: blocks a commit that holds API-key shapes, private keys, `api_key = "..."` lines or a `.env` file |
| `demo_bad.py` / `demo_good.py` | a file with a FAKE key (what not to do) and the fixed version |
| `.env.example`, `.gitignore.example`, `pre-commit` | templates: key names only, keep `.env` out of git, the one-line hook |

## Run app_basics.py (Windows cmd)
```
python app_basics.py
set SHOPBOT_API_KEY=demo-key-123
python app_basics.py
```
(macOS / Linux: `SHOPBOT_API_KEY=demo-key-123 python3 app_basics.py`)

Output (tested 2026-11-07, Python 3):
```
Stopped: SHOPBOT_API_KEY is not set (put it in .env).

Key loaded: demo****
asha    view_own_order  ALLOW
asha    refund          DENY
meena   refund          ALLOW
nobody  view_own_order  DENY
OK      'Where is my order?'
REJECT  too long (max 2000 chars)
OK      'ORD-123456'
REJECT  bad order id 'ORD-12AB'
```

## Run secret_scan.py
By hand, on any files:
```
python secret_scan.py demo_bad.py demo_good.py
```
```
BLOCKED  demo_bad.py:2  OpenAI-style key
BLOCKED  demo_bad.py:2  Hard-coded secret
Commit stopped. Move secrets to .env. Rotate any key that leaked.
```
As a git hook (runs before every commit, exit code 1 stops the commit):
1. Copy `secret_scan.py` into your repo.
2. Copy `pre-commit` to `.git/hooks/pre-commit` (on macOS / Linux also run `chmod +x .git/hooks/pre-commit`; use `python3` there if `python` is not found).
3. `git add .` then `git commit -m "..."`: a commit with a key is blocked; once the key is in `.env` the hook prints `OK: 3 files checked, no secrets found` and the commit goes through (tested in a fresh repo).

## Notes
* The key in `demo_bad.py` is made up. Never paste a real key into a demo.
* `login()` is simplified (no password check) so the demo stays short. In a real app use a proven login library or provider.
* This scanner is a teaching version. For real projects also look at tools like gitleaks or your Git host's secret scanning.
* If a real key ever leaks: revoke it first, create a new one, check usage and the bill, then clean the git history.
* Defensive use only. Test only apps you own or have permission to test.
