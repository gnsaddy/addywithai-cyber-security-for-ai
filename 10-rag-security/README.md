# Lecture 10, RAG Security: demo code

A tiny RAG index with a permission filter on retrieval, plus a checker that runs before documents enter the vector store.
Plain Python 3 (3.9+), standard library only. All documents are fake. Word overlap stands in for vector similarity, so no model or API key is needed.

| File | What it shows |
|---|---|
| `rag_guard.py` | `DOCS` (chunks with `teams` + `source`), `retrieve_naive()` (ranks every chunk for every user: the leak) vs `retrieve_safe()` (filter by the user's teams FIRST, then rank) |
| `ingest_check.py` | `check()` (untrusted source, hidden zero-width characters, instruction-like text using the harmless `TEST-INJECT` marker), `ingest()` (flagged docs go to quarantine, clean docs get a sha256 + source = provenance) |

## Run
```
python rag_guard.py
python ingest_check.py
```

Output (tested 2026-11-17, Python 3):
```
NAIVE: ['hr-7']
SAFE : []
SAFE : ['sales-2']
```
```
STORED      faq-2 help-center c63e4e74a851
QUARANTINED web-4 ['untrusted source', 'instruction-like text']
QUARANTINED faq-3 ['hidden characters']
```

## What to take away
* Filter chunks by the logged-in user before ranking; never filter the answer afterwards.
* In a real vector database, store permissions as metadata on every chunk and use its filter (or one namespace per customer).
* Retrieved text is data, not instructions: delimit it and never let it trigger tools.
* Defensive use only. Test only apps you own or have permission to test.
