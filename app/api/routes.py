import os
import time
from collections import defaultdict, deque

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

from app.chatbot.chatbot import chat

router = APIRouter()

MAX_MESSAGE_LENGTH = 2000
MAX_REQUESTS = 20
RATE_LIMIT_WINDOW = 60
request_times = defaultdict(deque)


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)


def check_rate_limit(client_id: str):
    now = time.time()
    timestamps = request_times[client_id]
    while timestamps and now - timestamps[0] >= RATE_LIMIT_WINDOW:
        timestamps.popleft()
    if len(timestamps) >= MAX_REQUESTS:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
        )
    timestamps.append(now)


@router.post("/chat")
def chat_endpoint(
    request: ChatRequest,
    x_api_key: str | None = Header(default=None),
    x_client_id: str | None = Header(default=None),
):
    expected_api_key = os.getenv("CHAT_API_KEY")
    if not expected_api_key:
        raise HTTPException(
            status_code=500,
            detail="Chat API authentication is not configured.",
        )
    if x_api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key.")

    client_id = x_client_id or x_api_key
    check_rate_limit(client_id)
    return chat(request.message, request.session_id)
