import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector
from psycopg_pool import ConnectionPool

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

SCHEMA_FILE = Path(__file__).resolve().parent.parent / "schema.sql"

# open=False: the pool opens only after the schema exists,
# because register_vector needs the "vector" extension to be there.
pool = ConnectionPool(
    DATABASE_URL,
    min_size=1,
    max_size=5,
    configure=register_vector,
    open=False,
)


def init_schema():
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute(SCHEMA_FILE.read_text(encoding="utf-8"))


def get_pool():
    if pool.closed:
        pool.open()
    return pool