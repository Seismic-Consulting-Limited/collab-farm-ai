import os

from dotenv import load_dotenv
from ollama import Client


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
)


MODEL = "gpt-oss:120b"


def generate_answer(messages):

    response = ""

    for chunk in client.chat(
        model=MODEL,
        messages=messages,
        stream=True,
    ):
        response += chunk["message"]["content"]

    return response