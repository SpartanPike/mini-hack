# src/rag/retriever.py
import faiss
import json
import numpy as np

from src.config import VECTOR_STORE_DIR, TOP_K
from src.models.embeddings import EmbeddingModel

class RAGRetriever:
    def __init__(self):
        self.index = faiss.read_index(str(VECTOR_STORE_DIR / "index.faiss"))
        self.metadata = json.loads((VECTOR_STORE_DIR / "metadata.json").read_text())
        self.chunks = [
            json.loads(line)["text"]
            for line in (VECTOR_STORE_DIR / "chunks.jsonl").read_text().splitlines()
        ]
        self.embedder = EmbeddingModel()

    def retrieve(self, query):
        q_emb = self.embedder.encode([query]).astype(np.float32)
        distances, indices = self.index.search(q_emb, TOP_K)
        results = []
        for d, idx in zip(distances[0], indices[0]):
            results.append({
                "text": self.chunks[idx],
                "score": float(d),
                "doc_id": self.metadata[idx]["doc_id"]
            })
        return results
