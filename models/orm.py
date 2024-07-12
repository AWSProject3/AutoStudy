import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
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

    def __repr__(self):
            return f"<Quiz(id={self.id}, quiz={self.quiz}>"

class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    language = Column(String(50), nullable=False)
    create_date = Column(DateTime, unique=True, nullable=False)

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
