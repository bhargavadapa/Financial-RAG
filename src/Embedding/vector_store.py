#VECTOR.PY
import faiss
import pickle
import numpy as np
from pathlib import Path
from src.Utils.config import FAISS_INDEX_PATH, METADATA_PATH, EMBEDDING_DIR

def create_faiss_index(embeddings, chunks, force_rebuild=False):
    """
    Creates and saves a FAISS index.
    Returns: index, metadata
    """
    
    # Ensure directory exists
    EMBEDDING_DIR.mkdir(parents=True, exist_ok=True)

    # Safety check
    if embeddings is None or len(embeddings) == 0:
        raise ValueError("Embeddings are empty. Cannot build FAISS index.")

    # Convert to numpy float32
    embeddings = np.array(embeddings).astype("float32")

    if len(embeddings.shape) != 2:
        raise ValueError("Embeddings must be 2D array.")

    dimension = embeddings.shape[1]

    # Skip rebuild if exists and not forced
    if FAISS_INDEX_PATH.exists() and METADATA_PATH.exists() and not force_rebuild:
        print("FAISS index already exists. Skipping rebuild.")
        return load_faiss_index()

    # Create FAISS index
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save index
    faiss.write_index(index, str(FAISS_INDEX_PATH))

    # Save metadata
    metadata = {
        "chunks": chunks,
        "dimension": dimension,
        "total_vectors": len(embeddings)
    }

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print(f"FAISS index created successfully with {len(embeddings)} vectors.")
    
    return index, metadata

def load_faiss_index():
    """
    Loads FAISS index and metadata safely.
    """
    if not FAISS_INDEX_PATH.exists() or not METADATA_PATH.exists():
        raise FileNotFoundError(
            "FAISS index not found. Please build the pipeline first."
        )

    # Load index
    index = faiss.read_index(str(FAISS_INDEX_PATH))

    # Load metadata
    with open(METADATA_PATH, "rb") as f:
        metadata = pickle.load(f)

    # Validate metadata
    if "chunks" not in metadata or "dimension" not in metadata:
        raise ValueError("Metadata file is corrupted.")

    # Validate dimension match
    if index.d != metadata["dimension"]:
        raise ValueError("FAISS index dimension mismatch with metadata.")

    return index, metadata

def initialize_faiss(embeddings, chunks, force_rebuild=False):
    """
    Auto-create FAISS index if not present.
    """
    if not FAISS_INDEX_PATH.exists() or not METADATA_PATH.exists() or force_rebuild:
        return create_faiss_index(embeddings, chunks, force_rebuild=True)

    return load_faiss_index()