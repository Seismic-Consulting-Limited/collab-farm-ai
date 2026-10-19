import numpy as np
from sentence_transformers import SentenceTransformer

from app.db import get_pool

model = SentenceTransformer("all-MiniLM-L6-v2")

SEARCH_SQL = """
SELECT content, source, embedding <=> %s AS distance
FROM knowledge_chunks
ORDER BY embedding <=> %s
LIMIT %s
"""


def search_knowledge(question, top_k=8):
    query = np.array(model.encode(question), dtype=np.float32)

    with get_pool().connection() as conn:
        rows = conn.execute(SEARCH_SQL, (query, query, top_k)).fetchall()

    return [
        {"content": content, "source": source, "distance": float(distance)}
        for content, source, distance in rows
    ]