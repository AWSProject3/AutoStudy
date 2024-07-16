from fastapi import WebSocket

from domains.conv_history_manager import ConversationHistoryManager
from domains.generative_ai import GenerativeAI
from domains.message_processor import MessageProcessor 
from core.connection_manager import ConnectionManager
from core.websocket_handler import WebSocketHandler
from models.user import UserContext

class QnAService:
    def __init__(
            self,
            history_manager: ConversationHistoryManager,
            ai_model: GenerativeAI,
            connection_manager: ConnectionManager
        ):
        self.history_manager = history_manager
        self.connection_manager = connection_manager
        self.message_processor = MessageProcessor(history_manager, ai_model)
        self.websocket_handler = WebSocketHandler(connection_manager, history_manager, self.message_processor)

    async def handle_websocket(self, websocket: WebSocket, current_user: dict):
        print(f"Current user: {current_user}")
        user = UserContext.from_dict(current_user) if current_user else None
        await self.websocket_handler.handle(websocket, user)
