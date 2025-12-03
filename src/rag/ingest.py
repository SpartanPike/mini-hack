# src/rag/ingest.py
import faiss
import json
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm

from src.config import RAW_DOCS_DIR, VECTOR_STORE_DIR, CHUNK_SIZE, CHUNK_OVERLAP
from src.models.embeddings import EmbeddingModel

def load_documents():
    docs = []
    for path in RAW_DOCS_DIR.glob("**/*"):
        if path.suffix.lower() in {".txt", ".md"}:
            docs.append({"id": str(path), "text": path.read_text()})
    return docs

def chunk_text(text, size, overlap):
    tokens = text.split()
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + size
        chunks.append(" ".join(tokens[start:end]))
        start = end - overlap
    return chunks

def build_vector_store():
    docs = load_documents()
    print(f"Loaded {len(docs)} docs.")
    em = EmbeddingModel()

    all_chunks = []
    metadata = []

    for doc in tqdm(docs, desc="Chunking documents"):
        chunks = chunk_text(doc["text"], CHUNK_SIZE, CHUNK_OVERLAP)
        for i, ch in enumerate(chunks):
            all_chunks.append(ch)
            metadata.append({
                "doc_id": doc["id"],
                "chunk_id": i
            })

    print(f"Total chunks: {len(all_chunks)}")

    embeddings = em.encode(all_chunks)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # IMPORTANT: faiss requires a STRING path!
    faiss.write_index(index, str(VECTOR_STORE_DIR / "index.faiss"))

    (VECTOR_STORE_DIR / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )

    (VECTOR_STORE_DIR / "chunks.jsonl").write_text(
        "\n".join(json.dumps({"text": c}) for c in all_chunks),
        encoding="utf-8"
    )

    print("Vector DB built successfully.")

if __name__ == "__main__":
    build_vector_store()
