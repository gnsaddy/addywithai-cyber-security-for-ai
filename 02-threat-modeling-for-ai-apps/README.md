# threat_model.py: Lecture 2, Threat Modeling for AI Apps

A tiny STRIDE threat model for **ShopBot**, the toy online-shop chatbot from the lecture
(chat + help-doc RAG + an order lookup tool + a refund tool).
Plain Python 3, standard library only. No installs, no API key, no network.

## Run
```
python threat_model.py
```

## Output (tested 2026-11-03, Python 3)
```
Threat model: ShopBot (6 threats)
 20  [E] Chat text makes the bot call the refund tool
 16  [T] Planted instructions in chat or help docs
 15  [I] Bot shows another customer's order
 12  [D] Long prompts and bots run up the bill
  9  [R] No record of who triggered a refund
  6  [S] Text pretends to be the system or an admin

Test checklist (top 3):
  [ ] Refunds over a limit need human approval
  [ ] A harmless planted line is ignored
  [ ] User A asks for user B's order: refused
```

## Try this
* Set `"logs_tool_calls": True` in `APP` and run again: the `[R]` threat disappears (5 threats).
* Describe your own app in `APP` (its flows, trust boundaries and tools) and change the scores.
* Add a rule for a new tool (for example a "send email" write tool).

## How it works
1. `APP` describes the app as data: flows (arrows of the data flow diagram, with a flag for "crosses a trust boundary"), tools (read or write) and whether tool calls are logged.
2. `RULES` holds one rule per STRIDE letter: the threat, a small check that says if it applies to this app, likelihood (1-5), impact (1-5) and the test to run.
3. The script keeps the rules that apply, scores them `likelihood x impact`, sorts highest first, and prints the ranked list plus a checklist for the top 3.

Scores are example judgements for a toy app. Defensive use only: test only apps you own or have permission to test.
