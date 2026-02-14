# Financial RAG

Retrieval-Augmented Generation (RAG) for financial time-series and company data - ingest, preprocess, embed, and query historical stock data with vector search.

## Overview

Financial RAG is a lightweight pipeline to convert CSV financial data into document embeddings, store them in a FAISS vector index, and run retrieval-augmented generation over that data. The project includes modules for data ingestion (Yahoo Finance CSVs), preprocessing and chunking, embedding generation, vector store management, and a retrieval/generation layer that can be used to answer questions about historical prices and company data.

Key components:

- `app.py`: Example entrypoint / demo runner.
- `requirements.txt`: Python dependencies.
- `src/Preprocessing/`: CSV-to-document conversion and chunking logic.
- `src/Embedding/`: Embedder and `vector_store.py` for FAISS index handling.
- `src/Ingestion/yahoo_finance.py`: Helpers for ingesting CSV stock data.
- `src/Retriever/`: Retriever and generator logic used for query-time RAG.
- `embeddings/faiss_index/index.faiss`: Example FAISS index (stored artifact).
- `tests/tests_preprocessing.py`: Unit tests for preprocessing.

## Features

- Ingest raw CSVs (raw/ folder) and convert rows to text documents.
- Chunk large documents for better retrieval relevance.
- Generate vector embeddings and persist them to a FAISS index.
- Query the vector store and synthesize answers using retrieved context.

## Getting Started

1. Create and activate a Python virtual environment (Windows example):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Prepare data:

- Place CSVs in `data/raw/` (some sample CSVs are already present).

4. Run the example app:

```powershell
python app.py
```

## Development

- Preprocessing code lives in `src/Preprocessing/` — see `csv_to_docs.py` and `chunking.py`.
- Embedding utilities live in `src/Embedding/` — update or swap embedder implementation in `embedder.py`.
- The vector store uses FAISS; you can find an example index at `embeddings/faiss_index/index.faiss`.

Run tests:

```powershell
python -m pytest -q
```

## Suggestions / Next Steps

- Add a `README` section with example queries and expected outputs.
- Add CI to run tests and linting on push.
- Add a short `CONTRIBUTING.md` and a license file.

## License

Add a license file (e.g., MIT) if you plan to open-source the repository.

---

If you want, I can (choose one):

- expand the README with example queries and sample responses,
- add a `CONTRIBUTING.md` and `LICENSE`, or
- create a GitHub Actions workflow to run tests on push.

Tell me which and I'll implement it.
