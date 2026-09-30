import chromadb

from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Connect to ChromaDB V5
client = chromadb.PersistentClient(
    path="knowledge/chroma_db"
)


collection = client.get_collection(
    name="collabfarm_knowledge_v7"
)


def search_knowledge(question, top_k=8):

    # Convert question into embedding
    question_embedding = model.encode(
        question
    ).tolist()


    # Search ChromaDB
    results = collection.query(
        query_embeddings=[
            question_embedding
        ],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )




    documents = results["documents"][0]

    sources = results["metadatas"][0]


    retrieved = []


    for document, source in zip(
        documents,
        sources
    ):

        retrieved.append(
            {
                "content": document,
                "source": source["source"]
            }
        )


    return retrieved