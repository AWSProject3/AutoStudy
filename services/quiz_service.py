
from domains.quiz_grader import QuizGrader
from models.repository import QuizRepository
from schemas.quiz.request import GenerateQuizRequest
from domains.quiz_generator import QuizGenerator
from schemas.quiz.response import CategoryDetails, GenerateQuizResponse, HintDetails


class QuizService:
    def __init__(self, request: GenerateQuizRequest, repo: QuizRepository, user: dict):
        self.request = request
        self.repo = repo
        self.user = user

    def create_quiz(self) -> GenerateQuizResponse:

        # generate quiz
        generator = QuizGenerator(self.request)
        response = generator.create_quiz()

        # save db
        repository = QuizRepository(session=self.repo.session)
        repository.save_quiz(quiz_data=response, user=self.user)

        return response
    
    def grade_quiz(self):

        # grade quiz
        grader = QuizGrader(self.request)
        response = grader.grade_quiz()

        # save db
        repository = QuizRepository(session=self.repo.session)
        repository.save_feedback(feedback_data=response)

        return response
    
    def get_quiz_history(self):
        repository = QuizRepository(session=self.repo.session)
        quizzes = repository.get_quiz_list(user=self.user)

        return [GenerateQuizResponse(
            source_language=quiz.source_language,
            target_language=quiz.target_language,
            difficulty=quiz.difficulty,
            category=CategoryDetails(
                type=quiz.category_type,
                detail=quiz.category_detail
            ),
            quiz=quiz.quiz,
            hint=HintDetails(
                source_language_code=quiz.hint_source_language_code,
                describe=quiz.hint_description
            ),
            answer=quiz.answer_code
        ) for quiz in quizzes]
        

        
