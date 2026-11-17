# rag_guard.py: mini RAG with a permission filter. Stdlib, fake docs.
import re

DOCS = [  # every chunk carries who may read it + where it came from
    {"id": "faq-1", "teams": {"all"}, "source": "help-center",
     "text": "Refunds take 5 to 7 days after pickup."},
    {"id": "hr-7", "teams": {"hr"}, "source": "hr-drive",
     "text": "Salary bands 2026: L3 18 to 24 lakh."},
    {"id": "sales-2", "teams": {"sales"}, "source": "crm",
     "text": "Q3 discount for Acme is 12 percent."},
    {"id": "wiki-9", "teams": {"it"}, "source": "wiki",
     "text": "Office wifi guest password rotates monthly."},
]

STOP = {"the", "a", "is", "for", "what", "are", "of", "to", "in", "after"}

def words(text):
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOP

def score(query, doc):  # stand-in for vector similarity: shared words
    return len(words(query) & words(doc["text"]))

def retrieve_naive(query, k=2):  # ranks every chunk, for every user
    hits = sorted(DOCS, key=lambda d: -score(query, d))[:k]
    return [d for d in hits if score(query, d) > 0]

def retrieve_safe(query, user, k=2):  # filter FIRST, then rank
    allowed = [d for d in DOCS if d["teams"] & (user["teams"] | {"all"})]
    hits = sorted(allowed, key=lambda d: -score(query, d))[:k]
    return [d for d in hits if score(query, d) > 0]

if __name__ == "__main__":
    ravi = {"name": "Ravi", "teams": {"sales"}}
    q = "what are the salary bands for L3"
    print("NAIVE:", [d["id"] for d in retrieve_naive(q)])
    print("SAFE :", [d["id"] for d in retrieve_safe(q, ravi)])
    print("SAFE :", [d["id"] for d in retrieve_safe("discount for Acme", ravi)])
