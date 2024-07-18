from fastapi import APIRouter, Depends, WebSocket
from fastapi.security import APIKeyCookie

from core.connection_manager import ConnectionManager
from core.dependencies import get_current_user_ws
from domains.conv_history_manager import ConversationHistoryManager
from domains.generative_ai import GenerativeAI
from models.redis_manager import RedisManager
from services.qna_service import QnAService

router = APIRouter(prefix="/api/qna")
cookie_scheme = APIKeyCookie(name="access_token")

redis_manager = RedisManager()
history_manager = ConversationHistoryManager(redis_manager)
ai_model = GenerativeAI()
connection_manager = ConnectionManager()

qna_service = QnAService(history_manager, ai_model, connection_manager)

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: dict = Depends(get_current_user_ws),
):  
    await qna_service.handle_websocket(websocket, current_user)
