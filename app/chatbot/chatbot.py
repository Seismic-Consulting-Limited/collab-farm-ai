from app.retrieval.retriever import search_knowledge
from app.chatbot.ollama_client import generate_answer
from app.chatbot.memory import add_message, get_history


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
    normalized_question = question.strip().casefold()
    history = get_history(session_id)

    # Return the prior answer only when this exact question has a
    # corresponding assistant message immediately after it.
    for index, message in enumerate(history):
        if (
            message.get("role") == "user"
            and message.get("content", "").strip().casefold()
            == normalized_question
        ):
            if index + 1 < len(history):
                next_message = history[index + 1]
                if next_message.get("role") == "assistant":
                    return {"answer": next_message["content"]}

    add_message(session_id, "user", question)

    documents = search_knowledge(question)
    context = "\n\n".join(doc["content"] for doc in documents)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(get_history(session_id))
    messages.append(
        {
            "role": "user",
            "content": (
                "Use the following CollabFarm knowledge to answer the question.\n\n"
                f"CollabFarm Context:\n{context}\n\n"
                f"Current Question:\n{question}"
            ),
        }
    )

    answer = generate_answer(messages)
    add_message(session_id, "assistant", answer)
    return {"answer": answer}
