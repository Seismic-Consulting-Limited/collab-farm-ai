import hashlib
from collections import Counter

import numpy as np

from app.db import get_pool, init_schema

UPSERT_SQL = """
INSERT INTO knowledge_chunks (id, source, content, content_hash, embedding)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (id) DO UPDATE SET
    source       = EXCLUDED.source,
    content      = EXCLUDED.content,
    content_hash = EXCLUDED.content_hash,
    embedding    = EXCLUDED.embedding,
    updated_at   = now()
"""


def store_embeddings(embedded_chunks):
    init_schema()

    rows = []
    position_in_source = Counter()

    for chunk in embedded_chunks:
        source = chunk["source"]
        position = position_in_source[source]
        position_in_source[source] += 1

        rows.append((
            f"{source}::{position}",
            source,
            chunk["content"],
            hashlib.sha256(chunk["content"].encode("utf-8")).hexdigest(),
            np.array(chunk["embedding"], dtype=np.float32),
        ))

    ids = [row[0] for row in rows]

    # one transaction: upsert everything, then delete chunks that no longer exist
    with get_pool().connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(UPSERT_SQL, rows)
            cur.execute("DELETE FROM knowledge_chunks WHERE id <> ALL(%s)", (ids,))

    return len(ids)