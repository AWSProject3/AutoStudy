import json

from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

from domains.conv_history_manager import ConversationHistoryManager
from domains.generative_ai import GenerativeAI
from core.connection_manager import ConnectionManager
from models.user import UserContext


class QnAService:
    def __init__(
            self,
            history_manager: ConversationHistoryManager,
            ai_model: GenerativeAI,
            connection_manager: ConnectionManager
        ):
        self.history_manager = history_manager
        self.ai_model = ai_model
        self.connection_manager = connection_manager

    async def handle_websocket(self, websocket: WebSocket, current_user: dict):
        print(f"Current user: {current_user}")
        user = UserContext.from_dict(current_user) if current_user else None
        if not await self.handle_connection(websocket, user):
            print("Failed to handle connection")
            return

        try:
            while True:
                if websocket.client_state == WebSocketState.DISCONNECTED:  # 연결이 끊어졌는지 주기적으로 체크
                    break
                try:
                    data = await websocket.receive_text()
                    response = await self.process_message(data, user)
                    await self.send_personal_message(response, user)
                except WebSocketDisconnect:
                    print(f"WebSocket disconnected for user: {user.email}")
                    break
                except RuntimeError as e:
                    if "disconnect" in str(e).lower():
                        print(f"WebSocket disconnected for user: {user.email}")
                        break
                    print(f"RuntimeError: {e}")
                    await self.send_personal_message(f"An error occurred: {str(e)}", user)
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    await self.send_personal_message(f"An error occurred: {str(e)}", user)
        finally: 
            self.disconnect(user)
            print(f"WebSocket connection closed for user: {user.email}")

    async def handle_connection(self, websocket: WebSocket, user: UserContext):
        if not user:
            await websocket.close(code=4001)
            return False
        
        
        await self.connection_manager.connect(websocket, user.email)
        self.history_manager.clear_history(user.email)
        return True

    async def disconnect(self, user: UserContext):
        await self.connection_manager.disconnect(user.email)
        self.history_manager.clear_history(user.email)

    async def process_message(self, message: str, user: UserContext):
        self.history_manager.add_message(user.email, "user", message)
        history = self.history_manager.get_history(user.email)

        # AI 모델에 전달할 때는 history를 그대로 사용
        response = self.ai_model.converse(history)
        
        # AI 응답을 저장할 때는 텍스트만 추출하여 저장
        ai_response_text = response["content"][0]["text"] if isinstance(response, dict) else response
        self.history_manager.add_message(user.email, "assistant", ai_response_text)

        return json.dumps({
            "user_input": message,
            "ai_response": response
        })

    async def send_personal_message(self, message: str, user: UserContext):
        await self.connection_manager.send_personal_message(message, user.email)


