# Fake News Detector using RAG 📰🔍

**A RAG-based fact-checker that grounds its verdicts in real labeled political claims, instead of just asking an LLM to guess.**

Built for my 5th semester ML course. Give it a claim, and it retrieves similar statements from the [LIAR dataset](https://www.cs.ucsb.edu/~william/data/liar_dataset.zip) (Wang, 2017, ACL), feeds them to GPT-4o-mini as context, and returns a verdict with reasoning — instead of a black-box "yes/no" with no grounding.

---

## How it works 🧩

1. **Preprocess** — the raw LIAR dataset (6 fine-grained labels: true, mostly-true, half-true, barely-true, false, pants-fire) gets binarized into `real` / `fake` for simplicity
2. **Embed** — all `real`-labeled statements get embedded locally (`sentence-transformers`) and stored in a persistent ChromaDB vector store
3. **Retrieve** — when a new claim comes in, it's embedded with the same model and matched against the most similar verified statements
4. **Generate** — those retrieved statements get passed to GPT-4o-mini as context, which returns a verdict (True/False/Unverified) + reasoning

```
claim → embed → retrieve similar verified facts → GPT-4o-mini + context → verdict
```

## Interfaces 🖥️

- **Flask API** (`app.py`) — `/api/check` endpoint, the backend for the web UI
- **React frontend** (`frontend/`) — clean Tailwind UI to submit a claim and see the verdict
- **CLI** (`src/main.py`) — quick terminal loop for testing without spinning up the web app

## Tech stack 🛠️

| Layer | Tech |
|---|---|
| Backend | Flask, Flask-CORS |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`, runs locally, no API cost) |
| Vector store | ChromaDB (persistent) |
| Frontend | React, Vite, Tailwind CSS |
| Dataset | LIAR — 12.8K labeled political statements |

## Running it locally 🚀

```bash
git clone https://github.com/zain-the-npc/Fake-News-Detector-using-RAG-.git
cd Fake-News-Detector-using-RAG-
pip install -r requirements.txt

# create .env with OPENAI_API_KEY=your-key-here

# one-time setup: preprocess data + build the vector store
python -m src.preprocess
python -m src.embedder

# run everything (Flask backend + React frontend together)
python run_project.py
```

This opens the app at `http://localhost:5173`. Alternatively, run `python -m src.main` for a terminal-only version.

## Why binarize the labels? 🤔   

LIAR's 6 labels aren't equally "fake" — half-true is a much softer judgment than pants-fire. For this project, `true` and `mostly-true` were grouped as **real**, everything else as **fake**. It's a simplification made for a course project, not a claim that half-true and pants-fire deserve identical treatment — a more nuanced version would keep the original 6-way labels or use a severity score.

## Dataset credit 📚

This project uses the LIAR dataset: William Yang Wang, *"Liar, Liar Pants on Fire": A New Benchmark Dataset for Fake News Detection*, ACL 2017. Original sources retain copyright of the data.

## More about this project 🔗

I wrote about the thinking behind this on LinkedIn: [linkedin.com/posts/zainthenpc_rag-explainableai-aiethics](https://www.linkedin.com/posts/zainthenpc_rag-explainableai-aiethics-ugcPost-7409959876484812800-yrzn/)
