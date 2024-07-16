from fastapi import Depends, HTTPException, Request, WebSocket, WebSocketException, status
from sqlalchemy.orm import Session

from core.cognito import AWSCognito
from interface.impl.cached_quiz import CachedQuizRepository
from models.connection import get_db
from models.redis_manager import RedisManager
from models.repository import QuizRepository
from services.auth_service import AuthService
from core.config import env_vars
from services.quiz_service import QuizService

def get_aws_cognito() -> AWSCognito:
    return AWSCognito()

def get_redis_manager():
    return RedisManager(host=env_vars.REDIS_HOST)

def get_quiz_repository(db_session: Session = Depends(get_db)):
    return QuizRepository(session=db_session)

def get_cached_quiz_repository(
    quiz_repo: QuizRepository = Depends(get_quiz_repository),
    redis_manager: RedisManager = Depends(get_redis_manager)
):
    return CachedQuizRepository(quiz_repo, redis_manager)

def get_quiz_service(cached_repo: CachedQuizRepository = Depends(get_cached_quiz_repository)):
    return QuizService(cached_repo)

def get_current_user(
    request: Request,
    cognito: AWSCognito = Depends(get_aws_cognito)
):
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_details = AuthService.verify_cognito_token(access_token, cognito)

    email = next((item['Value'] for item in user_details if item['Name'] == 'email'), None)
    name = next((item['Value'] for item in user_details if item['Name'] == 'name'), None)

    user_info = {
        'email': email,
        'name': name
    }

    return user_info


async def get_current_user_ws(
    websocket: WebSocket,
    cognito: AWSCognito = Depends(get_aws_cognito)
):
    access_token = websocket.cookies.get("access_token")
    
    if not access_token:
        print("No access token found")
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    
    try:
        user_details = AuthService.verify_cognito_token(access_token, cognito)

        email = next((item['Value'] for item in user_details if item['Name'] == 'email'), None)
        name = next((item['Value'] for item in user_details if item['Name'] == 'name'), None)

        user_info = {
            'email': email,
            'name': name
        }

        return user_info
    except Exception:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
