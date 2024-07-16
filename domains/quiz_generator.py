from typing import List
from interface.impl.cached_quiz import CachedQuizRepository
from schemas.quiz.request import GenerateQuizRequest
from domains import prompt_builder
from domains.generative_ai import GenerativeAI

class QuizGenerator:
    def __init__(self, 
                 request: GenerateQuizRequest, 
                 cached_repo: CachedQuizRepository, 
                 user: dict) -> None:
        self.source_language = request.source_language
        self.target_language = request.target_language
        self.difficulty = request.difficulty
        self.cached_repo = cached_repo
        self.user = user

    def get_recent_category_details(self) -> List[str]:
        return self.cached_repo.get_recent_category_details(self.user)

    def create_quiz(self):
        # get category_detail
        recent_categories = self.get_recent_category_details()
        
        # prompt build
        prompt = prompt_builder.build_prompt(
            template="create_quiz.txt",
            replacements={
                "source_language": self.source_language,
                "target_language": self.target_language,
                "difficulty": self.difficulty,
            },
            recent_categories=recent_categories
        )

        #call bedrock
        bedrock = GenerativeAI()
        response = bedrock.invoke_model(prompt)

        return response

