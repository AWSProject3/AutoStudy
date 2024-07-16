from typing import List
import json
from sqlalchemy.inspection import inspect

from interface.db_interface import DBInterface
from models.redis_manager import RedisManager
from models.repository import QuizRepository
from models.orm import Quiz

class CachedQuizRepository(DBInterface):
    def __init__(self, db_repo: QuizRepository, redis_manager: RedisManager):
        self.db_repo = db_repo
        self.redis_manager = redis_manager

    def get_quiz_list(self, user: dict) -> List[Quiz]:
        cache_key = f"quiz_list:{user['email']}"
        cached_data = self.redis_manager.get(cache_key)

        if cached_data:
            # Redis에서 데이터를 찾았으면 역직렬화하여 반환
            return [Quiz(**quiz_data) for quiz_data in json.loads(cached_data)]
        
        # Redis에 데이터가 없으면 DB에서 조회
        quiz_list = self.db_repo.get_quiz_list(user)
        
        # 조회한 데이터를 Redis에 캐싱
        # serialized_data = json.dumps([quiz.__dict__ for quiz in quiz_list])
        serialized_data = json.dumps([self.object_as_dict(quiz) for quiz in quiz_list])
        self.redis_manager.set(cache_key, serialized_data)

        return quiz_list

    def save_quiz(self, quiz_data: dict, user: dict) -> None:
        # db save
        self.db_repo.save_quiz(quiz_data, user)

        # Redis 캐시 무효화 (새 퀴즈가 추가되었으므로)
        cache_key = f"quiz_list:{user['email']}"
        self.redis_manager.delete(cache_key)

        # category_detail save Redis queue
        category_detail_key = f"category_detail_queue:{user['email']}"

        # quiz_data에서 category와 detail 정보 추출
        category = quiz_data.get('category', {})
        category_detail = category.get('detail') if isinstance(category, dict) else None

        if category_detail:  
            self.redis_manager.rpush_and_trim(category_detail_key, category_detail)

    def get_recent_category_details(self, user: dict) -> list:

        # 사용자의 최근 7개 category_detail을 가져옵니다.        
        category_detail_key = f"category_detail_queue:{user['email']}"
        return self.redis_manager.get_list(category_detail_key)
    
    def object_as_dict(self, obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}
