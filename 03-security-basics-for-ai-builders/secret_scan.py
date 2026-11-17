# secret_scan.py: block a git commit if it contains secrets. Stdlib only.
# Hook: put "python secret_scan.py" in .git/hooks/pre-commit
import re, subprocess, sys

PATTERNS = {
    "OpenAI-style key": r"sk-[A-Za-z0-9_-]{20,}",
    "AWS access key": r"AKIA[0-9A-Z]{16}",
    "Private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "Hard-coded secret": r"(?i)(api_key|secret|password|token)\s*=\s*['\"].{8,}",
}

def staged_files():  # the files you are about to commit
    out = subprocess.run(["git", "diff", "--cached", "--name-only"],
                         capture_output=True, text=True)
    return [f for f in out.stdout.splitlines() if f]

def scan(paths):
    found = []
    for path in paths:
        if path.endswith(".env"):
            found.append((path, 0, ".env file (keep it out of git)"))
            continue
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue  # deleted or not a file
        for n, line in enumerate(text.splitlines(), 1):
            for name, pattern in PATTERNS.items():
                if re.search(pattern, line):
                    found.append((path, n, name))
    return found

if __name__ == "__main__":
    paths = sys.argv[1:] or staged_files()
    found = scan(paths)
    for path, n, name in found:
        where = f"{path}:{n}" if n else path
        print(f"BLOCKED  {where}  {name}")
    if found:
        print("Commit stopped. Move secrets to .env. Rotate any key that leaked.")
        sys.exit(1)
    print(f"OK: {len(paths)} files checked, no secrets found")
