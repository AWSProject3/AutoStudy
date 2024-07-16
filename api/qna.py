from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.security import APIKeyCookie

from core.connection_manager import ConnectionManager
from core.dependencies import get_current_user, get_current_user_ws
from domains.conv_history_manager import ConversationHistoryManager
from domains.generative_ai import GenerativeAI
from models.redis_manager import RedisManager
from models.user import UserContext
from services.qna_service import QnAService

router = APIRouter(prefix="/api/qna")
cookie_scheme = APIKeyCookie(name="access_token")

redis_manager = RedisManager()
history_manager = ConversationHistoryManager(redis_manager)
ai_model = GenerativeAI()
connection_manager = ConnectionManager()

qna_service = QnAService(history_manager, ai_model, connection_manager)

# @router.websocket("/ws")
# async def websocket_endpoint(
#     websocket: WebSocket,
#     current_user: dict = Depends(get_current_user_ws),
# ):  
#     await qna_service.handle_websocket(websocket, current_user)

#     try:
#         while True:
#             data = await websocket.receive_text()
#             response = await qna_service.process_message(data, current_user)
#             await qna_service.send_personal_message(response, current_user)
#     except WebSocketDisconnect:
#         qna_service.disconnect(current_user)
@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user: dict = Depends(get_current_user_ws),
):  
    await qna_service.handle_websocket(websocket, current_user)
