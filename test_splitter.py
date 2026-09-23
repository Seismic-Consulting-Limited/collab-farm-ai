from app.ingestion.loader import load_markdown_documents
from app.ingestion.splitter import split_documents


documents = load_markdown_documents(
    "knowledge/raw"
)


chunks = split_documents(
    documents
)


print(
    f"Created {len(chunks)} chunks"
)


for chunk in chunks[:5]:

    print("----------------")
    print(chunk["source"])
    print(chunk["content"][:200])