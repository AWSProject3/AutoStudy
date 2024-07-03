from models.repository import QuizRepository
from schemas.quiz.request import GenerateQuizRequest
from domains import prompt_builder
from domains.generative_ai import GenerativeAI

class QuizGenerator:
    def __init__(self, request: GenerateQuizRequest) -> None:
        self.source_language = request.source_language
        self.target_language = request.target_language
        self.difficulty = request.difficulty

    def create_quiz(self):
        # prompt build
        prompt = prompt_builder.build_prompt(
            replacements={
                "source_language": self.source_language,
                "target_language": self.target_language,
                "difficulty": self.difficulty,
            }
        )

        #call bedrock
        bedrock = GenerativeAI()
        response = bedrock.invoke_model(prompt)

        return response

