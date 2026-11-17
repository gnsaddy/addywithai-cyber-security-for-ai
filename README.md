# Cyber Security for AI: code for every lecture

Python code for the **Cyber Security for AI** series by **@addywithai**. Each folder matches one lecture and has its own `README.md`.

## How to run any lecture

```bash
cd <folder>
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt   # if the folder has one
cp .env.example .env              # only if the folder has one, then paste your own key
```

Then follow the run steps in that folder's `README.md`. Never commit your `.env` file; it is already in `.gitignore`.

Python 3.10 or newer.

## Lectures

| # | Lecture | Code |
|---|---|---|
| 1 | AI Security Landscape | No code for this one |
| 2 | Threat Modeling for AI Apps | [02-threat-modeling-for-ai-apps](02-threat-modeling-for-ai-apps) |
| 3 | Security Basics for AI Builders | [03-security-basics-for-ai-builders](03-security-basics-for-ai-builders) |
| 4 | Securing Vibe-Coded Apps | [04-vibe-coding-security](04-vibe-coding-security) |
| 5 | Prompt Injection | [05-prompt-injection](05-prompt-injection) |
| 6 | Jailbreaks and Guardrails | [06-jailbreaks-and-guardrails](06-jailbreaks-and-guardrails) |
| 7 | Output Handling | [07-output-handling](07-output-handling) |
| 8 | Data Leakage | [08-data-leakage](08-data-leakage) |
| 9 | Privacy and Compliance | No code for this one |
| 10 | RAG Security | [10-rag-security](10-rag-security) |
| 11 | Securing AI Agents | [11-securing-ai-agents](11-securing-ai-agents) |
| 12 | MCP and Tool Supply-Chain Risks | [12-mcp-tool-supply-chain](12-mcp-tool-supply-chain) |
| 13 | Securing Multi-Agent and Browser/Computer-Use Agents | Coming soon |
| 14 | Insecure AI-Generated Code and Hallucinated Packages | Coming soon |
| 15 | API Key, Cost and Abuse Protection | Coming soon |
| 16 | Model and Data Supply Chain | Coming soon |
| 17 | Securing Deployment | Coming soon |
| 18 | Securing the CI/CD Pipeline | Coming soon |
| 19 | Monitoring, Logging and Incident Response | Coming soon |
| 20 | Red-Teaming and Safety Evals | Coming soon |
| 21 | OWASP LLM Top 10 Checklist | Coming soon |
| 22 | Capstone: Hardening a Full AI App End to End | Coming soon |
