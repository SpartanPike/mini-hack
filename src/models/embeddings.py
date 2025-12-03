# src/models/embeddings.py
from typing import List
from sentence_transformers import SentenceTransformer
from src.config import EMBEDDING_MODEL_NAME

class EmbeddingModel:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    def encode(self, texts: List[str]):
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
