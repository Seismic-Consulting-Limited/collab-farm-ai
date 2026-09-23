import chromadb


client = chromadb.PersistentClient(
    path="knowledge/chroma_db"
)


collection = client.get_or_create_collection(
    name="collabfarm_knowledge_v5"
)


def store_embeddings(embedded_chunks):

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for index, chunk in enumerate(embedded_chunks):

        ids.append(
            str(index)
        )

        documents.append(
            chunk["content"]
        )

        embeddings.append(
            chunk["embedding"]
        )

        metadatas.append(
            {
                "source": chunk["source"]
            }
        )


    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


    return len(ids)