from src.Preprocessing.chunking import chunk_documents

def test_chunking():
    docs = ["Stock price increased significantly today."]
    chunks = chunk_documents(docs)

    assert isinstance(chunks, list)
    assert len(chunks) > 0
