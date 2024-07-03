
from models.repository import QuizRepository
from schemas.quiz.request import GenerateQuizRequest
from domains.quiz_generator import QuizGenerator
from schemas.quiz.response import GenerateQuizResponse


class QuizService:
    def __init__(self, request: GenerateQuizRequest, repo: QuizRepository):
        self.request = request
        self.repo = repo

    def create_quiz(self) -> GenerateQuizResponse:
        generator = QuizGenerator(self.request)
        
        response = generator.create_quiz()

        # save db
        repository = QuizRepository(session=self.repo.session)
        repository.save_quiz(quiz_data=response)

        return response
    
    def grade_quiz(self):
        pass