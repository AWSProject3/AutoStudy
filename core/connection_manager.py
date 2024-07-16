from fastapi import WebSocket
from fastapi.websockets import WebSocketState


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        try:
            await websocket.accept()
            self.active_connections[client_id] = websocket
        except Exception as e:
            print(f"Error accepting WebSocket connection: {str(e)}")
            raise

    async def disconnect(self, client_id: str): # 메서드를 비동기로 -> WebSocket을 명시적으로 닫기
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            if websocket.client_state == WebSocketState.CONNECTED:
                try:
                    await websocket.close()
                except RuntimeError as e:
                    print(f"Error closing WebSocket for {client_id}: {str(e)}")
            del self.active_connections[client_id]
            print(f"WebSocket connection closed for client: {client_id}")

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            try:
                await websocket.send_text(message)
            except RuntimeError as e:
                print(f"Error sending message to client {client_id}: {e}")
                await self.disconnect(client_id)

    def get_active_connection(self, client_id: str) -> WebSocket:
        return self.active_connections.get(client_id)
    
    def is_connected(self, client_id: str) -> bool:
        return client_id in self.active_connections and self.active_connections[client_id].client_state == WebSocketState.CONNECTED