from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text


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

    def __repr__(self):
            return f"<Quiz(id={self.id}, quiz={self.quiz}>"

