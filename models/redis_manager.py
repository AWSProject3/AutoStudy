import redis

from core.config import env_vars

REDIS_HOST = env_vars.REDIS_HOST
CONVERSATION_TTL = 86400

class RedisManager:
    def __init__(self, host=REDIS_HOST, port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def set(self, key: str, value: str, ex=CONVERSATION_TTL):
        self.redis_client.set(key, value, ex=ex)

    def get(self, key: str) -> str:
        return self.redis_client.get(key)

    def delete(self, key: str):
        self.redis_client.delete(key)

    def exists(self, key: str) -> bool:
        return self.redis_client.exists(key)
    
    def ttl(self, key: str) -> int:
        return self.redis_client.ttl(key)
    
    def rpush_and_trim(self, key: str, value: str, max_length: int = 7):
        pipe = self.redis_client.pipeline()
        pipe.rpush(key, value)
        pipe.ltrim(key, -max_length, -1)
        pipe.execute()

    def get_list(self, key: str) -> list:
        return self.redis_client.lrange(key, 0, -1)

