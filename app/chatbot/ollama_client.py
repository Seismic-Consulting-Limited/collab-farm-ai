import os

from dotenv import load_dotenv
from ollama import Client, ResponseError


load_dotenv()


API_KEY = os.getenv("OLLAMA_API_KEY")

if not API_KEY:
    raise ValueError(
        "OLLAMA_API_KEY is not set"
    )


client = Client(
    host="https://ollama.com",
    headers={
        "Authorization": f"Bearer {API_KEY}"
    },
    timeout=30.0,
)


MODEL = "gpt-oss:120b"


def generate_answer(messages):

    try:

        response = ""

        for chunk in client.chat(
            model=MODEL,
            messages=messages,
            stream=True,
        ):
            response += chunk["message"]["content"]

        # Return the completed answer.
        return response

    except ResponseError as e:

        print(f"Ollama API error: {e}")

        return (
            "Sorry, I'm unable to answer your question "
            "right now. Please try again later."
        )

    except Exception as e:

        print(f"Ollama connection or timeout error: {e}")

        return (
            "Sorry, the CollabFarm assistant is temporarily "
            "unavailable. Please try again later."
        )
