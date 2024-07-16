from fastapi import APIRouter, Depends, Request, status

from core.dependencies import get_current_user, get_quiz_service
from models.repository import QuizRepository
from schemas.quiz.request import GenerateQuizRequest, GradeQuizRequest
from schemas.quiz.response import GenerateQuizResponse, GradeQuizResponse
from services.quiz_service import QuizService

router = APIRouter(prefix="/api/quiz")


@router.post("/generate", status_code=status.HTTP_201_CREATED, tags=["Quiz"])
def generate_quiz_handler(
    quiz_request: GenerateQuizRequest,
    current_user: dict = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service)
) -> GenerateQuizResponse:
    return quiz_service.create_quiz(quiz_request, current_user)

@router.post("/grade", status_code=status.HTTP_201_CREATED, tags=["Quiz"])
def grading_quiz_handler(
    request: GradeQuizRequest,
    current_user: dict = Depends(get_current_user),
    quiz_repo: QuizRepository = Depends(),
) -> GradeQuizResponse:

    response = QuizService(request, quiz_repo, current_user)
    return response.grade_quiz()

@router.get("/history", status_code=status.HTTP_200_OK, tags=["Quiz"])
def get_quiz_history(
    current_user: dict = Depends(get_current_user),
    quiz_service: QuizService = Depends(get_quiz_service)
) -> list[GenerateQuizResponse]:
    return quiz_service.get_quiz_history(current_user)


def get_grade_result():
    ...
