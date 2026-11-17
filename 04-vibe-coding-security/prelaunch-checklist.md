# Pre-launch security checklist (vibe-coded apps)

- [ ] No secrets in the code or in the git history (rotate any key that was ever committed)
- [ ] Auth is checked on the server, for every route
- [ ] Users can only see and change their own data
- [ ] Database rules are on (for example row level security), and the app does not use an admin key
- [ ] Every input is validated, and every query uses parameters
- [ ] Rate limits on login and on the API
- [ ] Packages are real, up to date, and scanned (pip-audit / npm audit / Dependabot)
- [ ] HTTPS everywhere, and error messages do not show internals

No app is 100% hack-proof. These habits block the most common attacks.
