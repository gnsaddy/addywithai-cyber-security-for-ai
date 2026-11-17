# notes_secure.py: the same app, fixed. Same features.
import os, re, time
from demo_db import make_db

# FIX 1: the secret comes from an environment variable
API_KEY = os.environ.get("NOTES_API_KEY")
if not API_KEY:
    raise SystemExit("Set NOTES_API_KEY first (see .env.example)")
db = make_db()

# FIX 4: accept only input that looks right
USERNAME = re.compile(r"[a-z]{1,20}")

def find_notes(owner):
    if not USERNAME.fullmatch(owner):
        raise ValueError("invalid username")
    # FIX 2: a parameter (?), never pasted text
    sql = "SELECT id, text FROM notes WHERE owner = ?"
    return db.execute(sql, (owner,)).fetchall()

def get_note(note_id, current_user):
    q = "SELECT owner, text FROM notes WHERE id = ?"
    row = db.execute(q, (note_id,)).fetchone()
    # FIX 3: check ownership on the server
    if row is None or row[0] != current_user:
        raise PermissionError("not your note")
    return row[1]

# FIX 5: a simple rate limit, 5 calls per minute per user
calls = {}
def allow(user, limit=5, window=60):
    now = time.time()
    recent = [t for t in calls.get(user, []) if now - t < window]
    calls[user] = recent + [now]
    return len(recent) < limit
