# src/config.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DOCS_DIR = DATA_DIR / "raw_docs"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# ---- GROQ LLM MODEL ----
# This is the Groq model ID.
# You can change this to test different Groq-hosted models, e.g.:
#   - "llama-3.3-70b-versatile"
#   - "llama-3.1-70b-versatile"
#   - "llama-3.1-8b-instant"
LLM_MODEL_NAME = "llama-3.3-70b-versatile"

# Embedding model (local, for RAG)
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# RAG settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 5
