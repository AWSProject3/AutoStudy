from typing import List, Text
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

class ScoreDetails(BaseModel):
    accuracy: int
    efficiency: int
    readability: int
    pep8_compliance: int
    modularity_reusability: int
    exception_handling: int

class FeedbackDetails(BaseModel):
    accuracy: str
    efficiency: str
    readability: str
    pep8_compliance: str
    modularity_reusability: str
    exception_handling: str

class GradeQuizResponse(BaseModel):
    score: ScoreDetails
    total_score: int
    summary: str
    detailed_feedback: FeedbackDetails
    positive_feedback: str
    suggestions: List[str]
    best_practice_code: str
    best_practice_explanation: str
