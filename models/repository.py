from fastapi import Depends
from sqlalchemy.orm import Session

from models.connection import get_db
from models.orm import Quiz, Profile
from schemas.quiz.response import GenerateQuizResponse

class QuizRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_quiz_list(self, user: dict) -> list[Quiz]:
        return self.session.query(Quiz).filter_by(user_email=user.get("email")).order_by(Quiz.id).all()

    def save_quiz(self, quiz_data: dict, user: dict) -> None:
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
            answer_code=quiz.answer,
            user_email=user.get("email")
        )
        self.session.add(db_quiz)
        self.session.commit()
        self.session.refresh(db_quiz)

    def save_feedback(self, feedback_data) -> None:
        pass

class ProfileRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_profile(self, email: str) -> Profile:
        return self.session.query(Profile).filter_by(email=email).first()

    def create_profile(self, profile_data: dict) -> None:
        
        profile = Profile.create(
            name=profile_data.get("name"),
            email=profile_data.get("email"),
            language=profile_data.get("language")
        )
        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)

        return profile

