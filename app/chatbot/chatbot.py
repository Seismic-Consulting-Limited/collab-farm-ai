from app.retrieval.retriever import search_knowledge
from app.chatbot.ollama_client import generate_answer
from app.chatbot.memory import (
    add_message,
    get_history
)


SYSTEM_PROMPT = """
You are CollabFarm AI Assistant.

Your job is to help users understand the CollabFarm platform.

Answer only using the provided CollabFarm knowledge.

Response guidelines:

- Write for normal platform users, not developers.
- Use simple and clear language.
- Do not mention documents, sources, files, retrieval, or knowledge bases.
- Do not use markdown tables unless the user asks for a table.
- Use headings and bullet points where helpful.
- Avoid overly technical language.
- Keep answers concise but informative.
- If information is unavailable, say:
  "The information is not available in the current CollabFarm knowledge."

Accuracy rules:

- Do not invent features or processes.
- Do not assume steps that are not documented.
- Do not create URLs, buttons, or registration procedures unless they exist in the knowledge.
- Always maintain a professional and helpful tone.
"""

def chat(question, session_id):

    # Store user's message in memory
    add_message(
        session_id,
        "user",
        question
    )


    # Retrieve relevant V5 CollabFarm knowledge
    documents = search_knowledge(
        question
    )


    # Combine retrieved knowledge
    context = "\n\n".join(
        [
            doc["content"]
            for doc in documents
        ]
    )


    # Collect source documents
    sources = list(
        set(
            [
                doc["source"]
                for doc in documents
            ]
        )
    )


    # Build messages for Ollama Cloud
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]


    # Add previous conversation history
    messages.extend(
        get_history(session_id)
    )


    # Add current question with retrieved context
    messages.append(
        {
            "role": "user",
            "content": f"""
Use the following CollabFarm knowledge to answer the question.

CollabFarm Context:

{context}


Current Question:

{question}
"""
        }
    )


    # Generate response using Ollama Cloud
    answer = generate_answer(
        messages
    )


    # Store assistant response in memory
    add_message(
        session_id,
        "assistant",
        answer
    )


    # Remove sources if answer says information is unavailable
    if (
        "The information is not available in the current CollabFarm knowledge."
        in answer
    ):
        sources = []


    return {
        "answer": answer,
        
    }