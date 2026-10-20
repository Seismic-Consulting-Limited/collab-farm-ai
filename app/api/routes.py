import logging
import os
import secrets

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from app.chatbot.chatbot import chat

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter()

SERVICE_KEY = os.getenv("SERVICE_KEY")


def require_service_key(x_service_key: str = Header(default="")):
    if not SERVICE_KEY:
        logger.error("SERVICE_KEY is not configured")
        raise HTTPException(status_code=503, detail="Service is not configured.")

    if not secrets.compare_digest(x_service_key.encode(), SERVICE_KEY.encode()):
        raise HTTPException(status_code=401, detail="Unauthorized")


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=1000)


@router.post("/chat", dependencies=[Depends(require_service_key)])
def chat_endpoint(request: ChatRequest):
    try:
        return chat(request.message, request.session_id)
    except Exception:
        logger.exception("Chat failed")
        raise HTTPException(
            status_code=503,
            detail="The assistant is temporarily unavailable. Please try again in a minute.",
        )