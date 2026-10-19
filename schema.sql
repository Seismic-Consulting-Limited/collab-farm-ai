CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS knowledge_chunks (
    id           text PRIMARY KEY,
    source       text        NOT NULL,
    content      text        NOT NULL,
    content_hash text        NOT NULL,
    embedding    vector(384) NOT NULL,
    updated_at   timestamptz NOT NULL DEFAULT now()
);