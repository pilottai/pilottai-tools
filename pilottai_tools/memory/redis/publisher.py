import json
from typing import Optional, List, Dict

from pilottai_tools.memory.redis.client import get_redis_client
from pilottai_tools.utils.logger import Logger


logger = Logger("Publisher")
client = get_redis_client()


def _key(chat_id: str) -> str:
    return f"chat:{chat_id}"


def create_conversation(chat_id: str) -> bool:
    """Initialize empty conversation list"""
    key = _key(chat_id)
    if not client.exists(key):
        return client.rpush(key, *[])
    return False


def add_message(chat_id: str, role: str, content: str) -> int:
    """Append a message to the conversation"""
    key = _key(chat_id)
    message = {"role": role, "content": content}
    return client.rpush(key, json.dumps(message))


def get_conversation(chat_id: str) -> List[Dict[str, str]]:
    """Get the full conversation as a list of messages"""
    key = _key(chat_id)
    messages = client.lrange(key, 0, -1)
    return [json.loads(msg) for msg in messages]


def delete_conversation(chat_id: str) -> int:
    """Delete conversation from Redis"""
    key = _key(chat_id)
    return client.delete(key)


def conversation_exists(chat_id: str) -> bool:
    """Check if conversation exists in Redis"""
    key = _key(chat_id)
    return client.exists(key) == 1


def export_conversation(chat_id: str) -> Optional[List[Dict[str, str]]]:
    """Retrieve and remove conversation (for storing in DB)"""
    if conversation_exists(chat_id):
        conv = get_conversation(chat_id)
        delete_conversation(chat_id)
        return conv
    return None
