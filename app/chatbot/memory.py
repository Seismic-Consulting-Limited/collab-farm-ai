chat_sessions = {}


def add_message(session_id, role, content):

    if session_id not in chat_sessions:
        chat_sessions[session_id] = []


    chat_sessions[session_id].append(
        {
            "role": role,
            "content": content
        }
    )


def get_history(session_id):

    if session_id not in chat_sessions:
        return []

    return chat_sessions[session_id]


def clear_memory(session_id):

    if session_id in chat_sessions:
        del chat_sessions[session_id]