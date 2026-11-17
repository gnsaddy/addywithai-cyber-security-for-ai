# Lecture 7, Output Handling: demo code

Three small tools that sit between a model and the places its text ends up (the "sinks"): the browser, a calculator and an action handler.
Plain Python 3, standard library only. The replies are canned test strings from a toy shop bot; **nothing is executed**. `example.com` / `example.net` hosts are reserved for examples.

| File | What it shows |
|---|---|
| `safe_output.py` | `render_unsafe()` vs `render_safe()` (`html.escape`), `safe_links()` (keep links to trusted hosts only), `safe_calc()` (parse math with `ast`, allow only numbers and + - * /, refuse everything else, never `eval`), `validate()` (JSON fields, allow-listed action, order ID pattern, amount range) |

## Run
```
python safe_output.py
```

Output (tested 2026-11-07, Python 3):
```
UNSAFE: <p>Your order ships today! <script>alert("test")</script></p>
SAFE:   <p>Your order ships today! &lt;script&gt;alert(&quot;test&quot;)&lt;/script&gt;</p>
LINKS:  Track: https://shop.example.com/t/981 ![img]([link removed])
CALC:   1299 * 0.9 -> 1169.1
CALC:   open("secrets.txt").read() -> BLOCKED, not allowed: Call
JSON:   OK refund
JSON:   REJECTED, amount 99999 out of range
JSON:   REJECTED, unknown action 'delete_all'
```

## What to take away
* Model output is untrusted input (OWASP LLM05, improper output handling). Check it at every sink.
* Browser: escape (or `textContent`), sanitize Markdown, check links and images, add a Content Security Policy.
* Code: never `eval`/`exec` model output. Use a safe parser, or a sealed sandbox (throwaway container, no network, time/memory limits) if you really must run code.
* Actions: ask for JSON, then validate every field and allow-list the action. Database: parameterized queries. Shell: fixed commands, arguments in a list.
* Defensive use only. Test only apps you own or have permission to test.
