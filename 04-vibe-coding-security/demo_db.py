# demo_db.py: a tiny in-memory database for the demo (nothing is saved to disk).
import sqlite3

def make_db():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE notes (id INT, owner TEXT, text TEXT)")
    db.executemany("INSERT INTO notes VALUES (?, ?, ?)",
                   [(1, "asha", "Buy milk"), (2, "ravi", "Bank PIN hint: dog")])
    return db
