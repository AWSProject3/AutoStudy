# import asyncio
# import json
# from fastapi import WebSocket, WebSocketDisconnect
# from fastapi.websockets import WebSocketState

# from core.connection_manager import ConnectionManager
# from domains.conv_history_manager import ConversationHistoryManager
# from domains.message_processor import MessageProcessor
# from models.user import UserContext

# class WebSocketHandler:
#     def __init__(
#         self,
#         connection_manager: ConnectionManager,
#         history_manager: ConversationHistoryManager,
#         message_processor: MessageProcessor
#     ):
#         self.connection_manager = connection_manager
#         self.history_manager = history_manager
#         self.message_processor = message_processor

#     async def handle(self, websocket: WebSocket, user: UserContext):
#         if not user:
#             await websocket.close(code=4001)
#             return

#         try:
#             await self.connection_manager.connect(websocket, user.email)

#             # 기존 대화 내용을 로드 or 새로운 대화 시작
#             history = self.history_manager.load_or_create_history(user.email)

#             if history:
#                 # 기존 대화 내용이 있다면 클라이언트에게 전송
#                 await self.connection_manager.send_personal_message(json.dumps({"type": "history", "content": history}), user.email)
            
#             while websocket.client_state != WebSocketState.DISCONNECTED:
#                 try:
#                     data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
#                     response = await self.message_processor.process(data, user)
#                     await self.connection_manager.send_personal_message(response, user.email)
#                 except asyncio.TimeoutError:
#                     # 타임아웃 발생 시 연결 상태 확인
#                     if websocket.client_state == WebSocketState.DISCONNECTED:
#                         break
#                 except WebSocketDisconnect:
#                     print(f"WebSocket disconnected for user: {user.email}")
#                     break
#                 except Exception as e:
#                     print(f"Error in WebSocket communication: {str(e)}")
#                     if websocket.client_state != WebSocketState.DISCONNECTED:
#                         await self.connection_manager.send_personal_message(f"An error occurred: {str(e)}", user.email)
#                     break
#         except Exception as e:
#             print(f"Unexpected error in WebSocket handler: {str(e)}")
#         finally: 
#             try:
#                 await self.connection_manager.disconnect(user.email)
#             except Exception as e:
#                 print(f"Error during disconnect for user {user.email}: {str(e)}")
#             print(f"WebSocket connection closed for user: {user.email}")

import json
import asyncio
from fastapi import WebSocket
from fastapi.websockets import WebSocketState, WebSocketDisconnect

from core.connection_manager import ConnectionManager
from domains.conv_history_manager import ConversationHistoryManager
from domains.message_processor import MessageProcessor
from models.user import UserContext

class WebSocketHandler:
    def __init__(
        self,
        connection_manager: ConnectionManager,
        history_manager: ConversationHistoryManager,
        message_processor: MessageProcessor
    ):
        self.connection_manager = connection_manager
        self.history_manager = history_manager
        self.message_processor = message_processor

    async def handle(self, websocket: WebSocket, user: UserContext):
        if not user:
            await websocket.close(code=4001)
            return

        try:
            await self.connection_manager.connect(websocket, user.email)

            # 기존 대화 내용을 로드 or 새로운 대화 시작
            history = self.history_manager.load_or_create_history(user.email)

            if history:
                # 기존 대화 내용이 있다면 클라이언트에게 전송
                await self.connection_manager.send_personal_message(json.dumps({"type": "history", "content": history}), user.email)
            
            while self.connection_manager.is_connected(user.email):
                try:
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=1.0)
                    response = await self.message_processor.process(data, user)
                    await self.connection_manager.send_personal_message(response, user.email)
                except asyncio.TimeoutError:
                    # 타임아웃 발생 시 연결 상태 확인
                    continue
                except WebSocketDisconnect:
                    print(f"WebSocket disconnected for user: {user.email}")
                    break
                except Exception as e:
                    print(f"Error in WebSocket communication: {str(e)}")
                    if websocket.client_state == WebSocketState.CONNECTED:
                        await self.connection_manager.send_personal_message(f"An error occurred: {str(e)}", user.email)
                    break
        except Exception as e:
            print(f"Unexpected error in WebSocket handler: {str(e)}")
        finally:
            if self.connection_manager.is_connected(user.email):
                await self.connection_manager.disconnect(user.email)
