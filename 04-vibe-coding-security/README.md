# Vibe-coded app security: demo code

From the YouTube video "Learn Vibe Coding Security: Why AI-Built Apps Get Hacked" (@addywithai, AI Engineer Roadmap bonus episode).

Plain Python 3 (3.8+). No installs, no API key, no network. Everything runs on a tiny **in-memory demo database** on your own machine.

| File | What it is |
|---|---|
| `notes_vulnerable.py` | A small notes app, the way AI often writes it. It works, but has 3 bugs: a hardcoded key, SQL built by pasting input, and no ownership check. **Do not ship code like this.** |
| `notes_secure.py` | The same app with 5 fixes: key from an environment variable, an allow list for usernames, a `?` parameter in SQL, an ownership check on the server, and a simple rate limit. |
| `demo_db.py` | Makes the demo database (two users: asha and ravi). |
| `demo.py` | Sends the same requests to both versions and prints the results. |
| `security-review-prompt.md` | Copy-paste prompts: ask for secure code, and ask the AI to review its own code. |
| `prelaunch-checklist.md` | The 8-point checklist from the video. |
| `.env.example`, `.gitignore` | How to keep secrets out of git. |

## Run it
```
python demo.py
```
Expected output:
```
== VULNERABLE ==
asha's notes:    [(1, 'Buy milk')]
odd input:       [(1, 'Buy milk'), (2, 'Bank PIN hint: dog')]
asha opens #2:   Bank PIN hint: dog

== SECURE ==
asha's notes:    [(1, 'Buy milk')]
odd input:       BLOCKED -> invalid username
asha opens #2:   BLOCKED -> not your note
7 quick calls:   [True, True, True, True, True, False, False]
```
`demo.py` sets a demo `NOTES_API_KEY` so it runs out of the box. In a real app, set the key outside the code (a `.env` file that is in `.gitignore`, your host's secret settings, or a secret manager). Run `python notes_secure.py` with no key set and it stops with a clear message.

## Real-world versions of each fix
- Secrets: environment variables / your host's secret store; rotate any key that was ever committed. Scan with gitleaks or GitHub secret scanning.
- SQL: always parameterized queries or an ORM; never f-strings or `+` with user input.
- Access control: check ownership on the server for every request; turn on database rules (for example Supabase row level security, Firebase security rules).
- Rate limits: use your framework's or gateway's rate limiter (the `allow()` function here only shows the idea; it lives in memory).
- Packages: check the name exists and is the one you meant before installing; scan with pip-audit, npm audit or Dependabot.

Only test security on apps you own or have written permission to test.
