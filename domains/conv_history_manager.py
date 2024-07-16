import json

from models.redis_manager import RedisManager

class ConversationHistoryManager:
    def __init__(self, redis_manager: RedisManager):
        self.redis_manager = redis_manager

    def _get_key(self, client_id: str) -> str:
        return f"conv_history:{client_id}"

    def get_history(self, client_id: str) -> list:
        key = self._get_key(client_id)
        history = self.redis_manager.get(key)
        return json.loads(history) if history else []

    def add_message(self, client_id: str, role: str, content: str):
        key = self._get_key(client_id)
        history = self.get_history(client_id)
        history.append({"role": role, "content": [{"text": content}]})
        self.redis_manager.set(key, json.dumps(history))

    def clear_history(self, client_id: str):
        key = self._get_key(client_id)
        self.redis_manager.delete(key)

    def history_exists(self, client_id: str) -> bool:
        key = self._get_key(client_id)
        return self.redis_manager.exists(key)
    
    def load_or_create_history(self, client_id: str) -> list:
        key = self._get_key(client_id)
        if self.redis_manager.exists(key):
            return self.get_history(client_id)
        return []