# 📈 Financial RAG: Stock Intelligence

**Financial RAG** is a specialized Retrieval-Augmented Generation pipeline designed for financial time-series and company data. It bridges the gap between raw historical CSVs and natural language insights.

The application allows users to input stock tickers, select analysis periods, and receive:
* **Interactive Visualizations**: High-fidelity charts for trend analysis.
* **Detailed Financial Reports**: Automated summaries of stock health.
* **Natural Language Q&A**: Direct answers to complex questions about stock performance, trends, and metrics using AI-driven context retrieval.

---

## ✨ Key Features

* **Semantic Financial Search**: Uses **FAISS** to retrieve historical context.
* **Time-Series Chunking**: Converts row-based CSV data into descriptive text documents.
* **Interactive Analytics**: Streamlit dashboard with **Plotly** charts.
* **Automated Reporting**: Synthesizes data into structured financial summaries.
* **Developer Friendly**: Modular architecture with automated CI/CD testing via GitHub Actions.
---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Interface** | Streamlit |
| **Vector Store** | FAISS |
| **Data Handling** | Pandas, Yahoo Finance API |
| **Orchestration** | Custom RAG Pipeline (`src/`) |
| **Visualization** | Plotly |
| **Testing** | Pytest, GitHub Actions |

---

## 🚀 Getting Started

### 1. Environment Setup
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux
```
### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### Run the Intellegence Hub
```powershell
streamlit run app.py
```

### 🧪 Development & Testing
```powershell
python -m pytest -q
```

### 📁 Project Architecture
```
├── src/
│   ├── Ingestion/       # Module for fetching data via YFinance or local CSVs
│   │   └── yahoo_finance.py
│   ├── Preprocessing/   # Transforms raw time-series into natural language docs
│   │   ├── csv_to_docs.py
│   │   └── chunking.py
│   ├── Embedding/       # Handles vectorization and FAISS index persistence
│   │   ├── embedder.py
│   │   └── vector_store.py
│   ├── Retriever/       # Logic for similarity search and context synthesis
│   │   ├── retriever.py
│   │   └── generator.py
│   └── Utils/           # Global constants, logging, and configuration
├── data/
│   ├── raw/             # Input folder for raw financial CSVs
│   └── processed/       # Metadata or temporary storage
├── embeddings/          # Directory where .faiss and .pkl files are stored
└── tests/               # Pytest suite for unit and integration testing

```

### Example Query

User: "How did AAPL perform during the banking crisis in March 2023?"

Financial RAG: "Based on retrieved historical data, AAPL showed resilience in March 2023, opening at $145.67 and closing at $164.90. This ~13% gain suggests a 'flight to quality' as the stock outperformed broader market indices."
