#EMBEDDER.PY
from sentence_transformers import SentenceTransformer
from src.Utils.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)

def create_embeddings(chunks):
    embeddings = model.encode(chunks)
    return embeddings
