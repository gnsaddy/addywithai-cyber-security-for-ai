# safe_output.py: treat model output as untrusted input. Stdlib only.
# Replies are canned test strings from a toy shop bot. Nothing here is executed.
import ast, html, json, operator, re

# 1) Rendering: the reply goes into a web page
REPLY = 'Your order ships today! <script>alert("test")</script>'

def render_unsafe(reply):
    return "<p>" + reply + "</p>"  # a browser would RUN that script

def render_safe(reply):
    return "<p>" + html.escape(reply) + "</p>"  # shown as plain text

TRUSTED_HOSTS = {"shop.example.com"}
URL = re.compile(r"https?://([^/\s)]+)[^\s)]*")

def safe_links(text):  # keep links only to hosts we trust
    return URL.sub(lambda m: m.group() if m.group(1) in TRUSTED_HOSTS
                   else "[link removed]", text)

# 2) Never eval() model output: allow numbers and + - * / only
OPS = {ast.Add: operator.add, ast.Sub: operator.sub,
       ast.Mult: operator.mul, ast.Div: operator.truediv}

def safe_calc(expr):
    def walk(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](walk(node.left), walk(node.right))
        raise ValueError("not allowed: " + type(node).__name__)
    return walk(ast.parse(expr, mode="eval").body)

# 3) Structured output: check every field before you act on it
ACTIONS = {"refund", "track"}

def validate(raw):
    data = json.loads(raw)  # must be valid JSON
    if set(data) != {"action", "order_id", "amount"}:
        raise ValueError("wrong fields")
    if data["action"] not in ACTIONS:
        raise ValueError(f"unknown action {data['action']!r}")
    if not re.fullmatch(r"ORD-\d{6}", str(data["order_id"])):
        raise ValueError("bad order_id")
    amount = data["amount"]
    if not isinstance(amount, (int, float)) or not 0 <= amount <= 5000:
        raise ValueError(f"amount {amount} out of range")
    return data

if __name__ == "__main__":
    print("UNSAFE:", render_unsafe(REPLY))
    print("SAFE:  ", render_safe(REPLY))
    print("LINKS: ", safe_links("Track: https://shop.example.com/t/981 "
                                "![img](https://pixel.example.net/p?d=981)"))
    for expr in ["1299 * 0.9", 'open("secrets.txt").read()']:
        try:
            print("CALC:  ", expr, "->", round(safe_calc(expr), 2))
        except ValueError as e:
            print("CALC:  ", expr, "-> BLOCKED,", e)
    for raw in ['{"action": "refund", "order_id": "ORD-123456", "amount": 499}',
                '{"action": "refund", "order_id": "ORD-123456", "amount": 99999}',
                '{"action": "delete_all", "order_id": "ORD-123456", "amount": 0}']:
        try:
            print("JSON:   OK", validate(raw)["action"])
        except ValueError as e:
            print("JSON:   REJECTED,", e)
