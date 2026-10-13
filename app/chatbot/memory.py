"""In-memory conversation storage with inactivity expiry.

This is suitable for a single-process MVP. Sessions are lost on restart and
are not shared between multiple workers; use a shared store for production.
"""
import time

chat_sessions = {}
session_last_activity = {}

MAX_HISTORY_MESSAGES = 10
SESSION_TTL_SECONDS = 30 * 60  # Expire after 30 minutes of inactivity.


def _expire_sessions(now=None):
    """Remove sessions that have been inactive for the configured TTL."""
    if now is None:
        now = time.time()

    expired = [
        session_id
        for session_id, last_activity in session_last_activity.items()
        if now - last_activity >= SESSION_TTL_SECONDS
    ]
    for session_id in expired:
        chat_sessions.pop(session_id, None)
        session_last_activity.pop(session_id, None)


def add_message(session_id, role, content):
    now = time.time()
    _expire_sessions(now)

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []

    chat_sessions[session_id].append({"role": role, "content": content})
    # Bound stored memory too, not just the history returned to the model.
    chat_sessions[session_id] = chat_sessions[session_id][-MAX_HISTORY_MESSAGES:]
    session_last_activity[session_id] = now


def get_history(session_id):
    now = time.time()
    _expire_sessions(now)

    if session_id not in chat_sessions:
        return []

    session_last_activity[session_id] = now
    return list(chat_sessions[session_id][-MAX_HISTORY_MESSAGES:])


def clear_memory(session_id):
    chat_sessions.pop(session_id, None)
    session_last_activity.pop(session_id, None)
