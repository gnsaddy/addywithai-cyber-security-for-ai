# Prompts for secure AI-written code

## 1. Ask for secure code (add this to your normal prompt)
```
Security rules for this code:
- Never put secrets (API keys, passwords) in the code. Read them from environment variables.
- Use parameterized queries for every database call. Never build SQL with string formatting.
- Check on the server, for every request, who the user is and that they own the data they ask for.
- Validate every input with an allow list (expected type, length, characters). Reject the rest.
- Add rate limits to login and to public API routes.
- Only use well-known packages, and tell me the exact package name and why.
Assume users will send bad input and will try to read other people's data.
Also write tests for the bad path: wrong user, strange input, too many requests.
```

## 2. Ask the AI to review its own code (open a NEW chat)
```
Review the code below as a security engineer.
List each issue as: line number, the problem, how serious it is, and the exact fix.
Check for: hardcoded secrets, injection (SQL, command), missing auth or ownership checks,
missing input validation, missing rate limits, unsafe or unknown packages,
and error messages that leak internal details.
Do not rewrite the whole file. Only list issues and fixes.

<paste the code here>
```
Then fix the issues and run the review again until it comes back clean.

An AI review is a helper, not a guarantee. Still read the code yourself and run real scanners (pip-audit / npm audit / Dependabot for packages, gitleaks / GitHub secret scanning for keys).
