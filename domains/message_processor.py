import json
from domains.conv_history_manager import ConversationHistoryManager
from domains.generative_ai import GenerativeAI
from models.user import UserContext

class MessageProcessor:
    def __init__(self, history_manager: ConversationHistoryManager, ai_model: GenerativeAI):
        self.history_manager = history_manager
        self.ai_model = ai_model

    async def process(self, message: str, user: UserContext):
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