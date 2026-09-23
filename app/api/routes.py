from fastapi import APIRouter
from pydantic import BaseModel

from app.chatbot.chatbot import chat


router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    message: str


@router.post("/chat")
def chat_endpoint(request: ChatRequest):

    response = chat(
        request.message,
        request.session_id
    )

    return response