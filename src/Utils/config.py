#CONFIG.PY
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

EMBEDDING_DIR = BASE_DIR / "embeddings" / "faiss_index"
FAISS_INDEX_PATH = EMBEDDING_DIR / "index.faiss"
METADATA_PATH = EMBEDDING_DIR / "metadata.pkl"

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
