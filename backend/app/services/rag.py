"""RAG pipeline: chunk -> embed (transformer) -> store -> cosine retrieval."""
import io
import re
from typing import List, Tuple
import numpy as np
from pypdf import PdfReader
from sqlalchemy.orm import Session
from .. import config, models

_model = None


def embedder():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer  # deep-learning encoder
        _model = SentenceTransformer(config.EMBED_MODEL)
    return _model


def embed(texts: List[str]) -> np.ndarray:
    return embedder().encode(texts, normalize_embeddings=True).astype("float32")


def extract_text(filename: str, data: bytes) -> str:
    if filename.lower().endswith(".pdf"):
        reader = PdfReader(io.BytesIO(data))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    return data.decode("utf-8", errors="ignore")


def chunk_text(text: str, size: int = 180, overlap: int = 40) -> List[str]:
    words = re.sub(r"\s+", " ", text).strip().split(" ")
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, max(len(words), 1), step) if words[i:i + size]]


def ingest(db: Session, user_id: int, doc: models.Document, text: str) -> int:
    chunks = chunk_text(text)
    if not chunks:
        return 0
    vectors = embed(chunks)
    db.add_all([
        models.Chunk(document_id=doc.id, user_id=user_id, chunk_index=i, text=c, embedding=v.tobytes())
        for i, (c, v) in enumerate(zip(chunks, vectors))
    ])
    return len(chunks)


def retrieve(db: Session, user_id: int, question: str, top_k: int = 4) -> List[Tuple[models.Chunk, float]]:
    rows = db.query(models.Chunk).filter(models.Chunk.user_id == user_id).all()
    if not rows:
        return []
    matrix = np.vstack([np.frombuffer(r.embedding, dtype="float32") for r in rows])
    scores = matrix @ embed([question])[0]  # cosine similarity (vectors are normalised)
    best = np.argsort(-scores)[:top_k]
    return [(rows[i], float(scores[i])) for i in best]
