import logging
from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session, joinedload, selectinload, contains_eager

from models.connection import get_db
from models.orm import FeedbackDetails, Grade, Quiz, Profile, ScoreDetails, Suggestion, UserInputCode
from schemas.quiz.request import GradeQuizRequest
from schemas.quiz.response import GenerateQuizResponse, GradeQuizResponse

class QuizRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_quiz_list(self, user: dict) -> List[Quiz]:
        return self.session.query(Quiz).filter_by(user_email=user.get("email")).order_by(Quiz.id).all()

    def save_quiz(self, quiz_data: dict, user: dict) -> Quiz:
        db_quiz = Quiz(
            source_language=quiz_data['source_language'],
            target_language=quiz_data['target_language'],
            difficulty=quiz_data['difficulty'],
            category_type=quiz_data['category']['type'],
            category_detail=quiz_data['category']['detail'],
            quiz=quiz_data['quiz'],
            hint_source_language_code=quiz_data['hint']['source_language_code'],
            hint_description=quiz_data['hint']['describe'],
            answer_code=quiz_data['answer'],
            user_email=user.get("email")
        )
        self.session.add(db_quiz)
        self.session.commit()
        self.session.refresh(db_quiz)

        return db_quiz


    def get_grade_result_by_quiz_id(self, quiz_id: int) -> Grade:
        
        grade = (
            self.session.query(Grade)
            .options(
                selectinload(Grade.score),
                selectinload(Grade.detailed_feedback),
                selectinload(Grade.user_input_code),
                selectinload(Grade.suggestions)
            )
            .filter(Grade.quiz_id == quiz_id)
            .first()
        )
        
        return grade

    def save_grade(self, grade_data: GradeQuizResponse, request_data: GradeQuizRequest, user_email: str) -> Grade:

        db_grade = Grade(
            total_score=grade_data['total_score'],
            summary=grade_data['summary'],
            positive_feedback=grade_data['positive_feedback'],
            best_practice_code=grade_data['best_practice_code'],
            best_practice_explanation=grade_data['best_practice_explanation'],
            source_language=request_data.source_language,
            target_language=request_data.target_language,
            difficulty=request_data.difficulty,
            quiz_id=request_data.id,
            user_email=user_email
        )

        db_score = ScoreDetails(**grade_data['score'])
        db_feedback = FeedbackDetails(**grade_data['detailed_feedback'])
        db_user_input_code = UserInputCode(code=request_data.user_input_code)

        db_grade.score = db_score
        db_grade.detailed_feedback = db_feedback
        db_grade.user_input_code = db_user_input_code

        for suggestion in grade_data['suggestions']:
            db_suggestion = Suggestion(content=suggestion)
            db_grade.suggestions.append(db_suggestion)

        self.session.add(db_grade)
        self.session.commit()
        self.session.refresh(db_grade)

        return db_grade


class GradeRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    


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

