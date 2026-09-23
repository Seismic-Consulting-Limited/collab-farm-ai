from app.retrieval.retriever import search_knowledge


question = (
    "How does an investor create an investment package?"
)


results = search_knowledge(
    question
)


print(
    f"Found {len(results)} results"
)


for result in results:

    print("----------------")
    print(
        result["source"]
    )

    print(
        result["content"][:300]
    )