# demo.py: run the same requests against both versions and compare.
# Everything runs on a tiny in-memory demo database on your own machine.
import os, sys
os.environ.setdefault("NOTES_API_KEY", "demo-key-from-env")  # in real life: set it outside the code
import notes_vulnerable as bad, notes_secure as good

odd_name = "x' OR '1'='1"  # an input that is not a normal username

print("== VULNERABLE ==")
print("asha's notes:   ", bad.find_notes("asha"))
print("odd input:      ", bad.find_notes(odd_name))
print("asha opens #2:  ", bad.get_note(2, "asha"))

print("\n== SECURE ==")
print("asha's notes:   ", good.find_notes("asha"))
for label, fn in [("odd input:      ", lambda: good.find_notes(odd_name)),
                  ("asha opens #2:  ", lambda: good.get_note(2, "asha"))]:
    try:
        print(label, fn())
    except (ValueError, PermissionError) as e:
        print(label, "BLOCKED ->", e)
print("7 quick calls:  ", [good.allow("asha") for _ in range(7)])
