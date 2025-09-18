import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHAT_DIR = os.path.join(BASE_DIR, "..", "chat_history")
os.makedirs(CHAT_DIR, exist_ok=True)

def _get_file_path(file_id: str) -> str:
    return os.path.join(CHAT_DIR, f"{file_id}.json")

def load_chat_history(file_id: str):
    """Load chat history for a given dataset (file_id)."""
    path = _get_file_path(file_id)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_chat_history(file_id: str, history: list):
    """Save the full chat history for a dataset."""
    path = _get_file_path(file_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def append_chat(file_id: str, query: str, response: str):
    """Append a single chat turn and persist it."""
    history = load_chat_history(file_id)
    history.append({
        "query": query,
        "response": response
    })
    save_chat_history(file_id, history)
