from app.ingestion.loader import load_markdown_documents
from app.ingestion.splitter import split_documents
from app.ingestion.embedder import create_embeddings


documents = load_markdown_documents(
    "knowledge/raw"
)


chunks = split_documents(
    documents
)


embedded_chunks = create_embeddings(
    chunks
)


print(
    f"Created {len(embedded_chunks)} embeddings"
)


print(
    embedded_chunks[0]["source"]
)


print(
    embedded_chunks[0]["embedding"][:5]
)