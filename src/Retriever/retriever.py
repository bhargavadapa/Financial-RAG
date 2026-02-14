#RETRIEVER.PY
import numpy as np
from sentence_transformers import SentenceTransformer
from src.Utils.config import EMBEDDING_MODEL
from src.Embedding.vector_store import load_faiss_index

from src.Embedding.embedder import create_embeddings

model = SentenceTransformer(EMBEDDING_MODEL)

def retrieve(query, top_k=20):
    """
    Retrieve top_k similar chunks from FAISS index.
    """

    index, metadata = load_faiss_index()
    stored_chunks = metadata["chunks"]

    if not isinstance(stored_chunks, list):
        raise ValueError("Stored chunks must be a list.")

    query_embedding = create_embeddings([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []
    for idx in indices[0]:
        if 0 <= int(idx) < len(stored_chunks):
            results.append(stored_chunks[int(idx)])

    return results
