#CHUNKING.PY
from src.Utils.config import CHUNK_SIZE, CHUNK_OVERLAP



def chunk_documents(documents):
    chunks = []
    for doc in documents:
        start = 0
        while start < len(doc):
            end = start + CHUNK_SIZE
            chunks.append(doc[start:end])
            start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks
