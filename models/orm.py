import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Float, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


Base = declarative_base()

class Quiz(Base):
    __tablename__ = 'quiz'

    id = Column(Integer, primary_key=True)
    source_language = Column(String(50), nullable=False)
    target_language = Column(String(50), nullable=False)
    difficulty = Column(String(50), nullable=False)
    category_type = Column(String(50), nullable=False)
    category_detail = Column(String(100), nullable=False)
    quiz = Column(Text, nullable=False)
    hint_source_language_code = Column(Text, nullable=False)
    hint_description = Column(Text, nullable=False)
    answer_code = Column(Text, nullable=False)
    user_email = Column(String(120), ForeignKey('profile.email'), nullable=False)

    profile = relationship("Profile", backref="quiz")
    grade = relationship("Grade", back_populates="quiz", uselist=False)

    def __repr__(self):
            return f"<Quiz(id={self.id}, quiz={self.quiz}>"

class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    language = Column(String(50), nullable=False)
    create_date = Column(DateTime, unique=True, nullable=False)

    grade = relationship("Grade", back_populates="profile")

    def __repr__(self):
        return f"<profile(id={self.id}, name={self.name}, language={self.language}>"
    
    @classmethod
    def create(cls, name: str, email: str, language: str) -> "Profile":
        return cls(
             name=name,
             email=email,
             language=language,
             create_date=datetime.datetime.now()
        )


class UserInputCode(Base):
    __tablename__ = 'user_input_codes'

    id = Column(Integer, primary_key=True)
    code = Column(Text, nullable=False)
    grade_id = Column(Integer, ForeignKey('grade.id'))

    grade = relationship("Grade", back_populates="user_input_code")


class ScoreDetails(Base):
    __tablename__ = 'score_details'

    id = Column(Integer, primary_key=True)
    accuracy = Column(Integer)
    efficiency = Column(Integer)
    readability = Column(Integer)
    pep8_compliance = Column(Integer)
    modularity_reusability = Column(Integer)
    exception_handling = Column(Integer)
    grade_id = Column(Integer, ForeignKey('grade.id'))

    grade = relationship("Grade", back_populates="score")

class FeedbackDetails(Base):
    __tablename__ = 'feedback_details'

    id = Column(Integer, primary_key=True)
    accuracy = Column(Text)
    efficiency = Column(Text)
    readability = Column(Text)
    pep8_compliance = Column(Text)
    modularity_reusability = Column(Text)
    exception_handling = Column(Text)
    grade_id = Column(Integer, ForeignKey('grade.id'))

    grade = relationship("Grade", back_populates="detailed_feedback")

class Grade(Base):
    __tablename__ = 'grade'

    id = Column(Integer, primary_key=True)
    total_score = Column(Integer)
    summary = Column(Text)
    positive_feedback = Column(Text)
    best_practice_code = Column(Text)
    best_practice_explanation = Column(Text)
    source_language = Column(String(50))
    target_language = Column(String(50))
    difficulty = Column(String(50))
    quiz_id = Column(Integer, ForeignKey('quiz.id'))
    user_email = Column(String(120), ForeignKey('profile.email'), nullable=False)

    profile = relationship("Profile", back_populates="grade")
    score = relationship("ScoreDetails", uselist=False, back_populates="grade")
    detailed_feedback = relationship("FeedbackDetails", uselist=False, back_populates="grade")
    suggestions = relationship("Suggestion", back_populates="grade")
    user_input_code = relationship("UserInputCode", uselist=False, back_populates="grade")
    quiz = relationship("Quiz", back_populates="grade", uselist=False)

class Suggestion(Base):
    __tablename__ = 'suggestions'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    grade_id = Column(Integer, ForeignKey('grade.id'))

    grade = relationship("Grade", back_populates="suggestions")

     