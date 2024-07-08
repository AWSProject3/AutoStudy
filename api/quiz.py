from fastapi import APIRouter, Depends
from models.repository import QuizRepository

from schemas.quiz.request import GenerateQuizRequest, GradeQuizRequest
from schemas.quiz.response import GenerateQuizResponse, GradeQuizResponse
from services.quiz_service import QuizService

router = APIRouter(prefix="/api/quiz")

@router.post("/generate", status_code=201)
def generate_quiz_handler(
    request: GenerateQuizRequest,
    quiz_repo: QuizRepository = Depends(),
) -> GenerateQuizResponse:
    return QuizService(request, quiz_repo).create_quiz()

@router.post("/grade", status_code=201)
def grading_quiz_handler(
    request: GradeQuizRequest,
    quiz_repo: QuizRepository = Depends(),
) -> GradeQuizResponse:

    response = QuizService(request, quiz_repo)
    return response.grade_quiz()
