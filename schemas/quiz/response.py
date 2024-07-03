from typing import Text
from pydantic import BaseModel

class HintDetails(BaseModel):
    source_language_code: Text
    describe: str

class CategoryDetails(BaseModel):
    type: str
    detail: str

class GenerateQuizResponse(BaseModel):
    source_language: str
    target_language: str
    difficulty: str
    category: CategoryDetails
    quiz: str
    hint: HintDetails
    answer: Text

class GradeQuizResponse(BaseModel):
    is_correct: bool