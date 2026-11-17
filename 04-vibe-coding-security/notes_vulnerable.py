# notes_vulnerable.py: typical AI-written code. DO NOT SHIP.
from demo_db import make_db  # tiny in-memory demo database

# BUG 1: a secret written right in the code
API_KEY = "sk-demo-1234-NOT-A-REAL-KEY"
db = make_db()  # two users: asha and ravi

def find_notes(owner):
    # BUG 2: user input pasted straight into the SQL text
    sql = f"SELECT id, text FROM notes WHERE owner = '{owner}'"
    return db.execute(sql).fetchall()

def get_note(note_id, current_user):
    q = "SELECT text FROM notes WHERE id = ?"
    # BUG 3: never checks that current_user owns this note
    return db.execute(q, (note_id,)).fetchone()[0]
