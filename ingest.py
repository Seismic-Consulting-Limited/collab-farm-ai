from app.ingestion.loader import load_markdown_documents
from app.ingestion.splitter import split_documents
from app.ingestion.embedder import create_embeddings
from app.vectorstore.chroma import store_embeddings


documents = load_markdown_documents(
    "knowledge/raw"
)


chunks = split_documents(
    documents
)


embedded_chunks = create_embeddings(
    chunks
)


stored = store_embeddings(
    embedded_chunks
)


print(
    f"Stored {stored} chunks in ChromaDB"
)