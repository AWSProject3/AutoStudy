from fastapi import Depends
from sqlalchemy.orm import Session

from models.connection import get_db
from models.orm import Quiz
from schemas.quiz.response import GenerateQuizResponse

class QuizRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def save_quiz(self, quiz_data: dict) -> None:
        quiz = GenerateQuizResponse(**quiz_data)
        db_quiz = Quiz(
            source_language=quiz.source_language,
            target_language=quiz.target_language,
            difficulty=quiz.difficulty,
            category_type=quiz.category.type,
            category_detail=quiz.category.detail,
            quiz=quiz.quiz,
            hint_source_language_code=quiz.hint.source_language_code,
            hint_description=quiz.hint.describe,
            answer_code=quiz.answer
        )
        self.session.add(db_quiz)
        self.session.commit()
        self.session.refresh(db_quiz)
        