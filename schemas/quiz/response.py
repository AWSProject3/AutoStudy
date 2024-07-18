from typing import List, Optional, Text
from pydantic import BaseModel

class HintDetails(BaseModel):
    source_language_code: Text
    describe: str

class CategoryDetails(BaseModel):
    type: str
    detail: str

class GenerateQuizResponse(BaseModel):
    id: int
    source_language: str
    target_language: str
    difficulty: str
    category: CategoryDetails
    quiz: str
    hint: HintDetails
    answer: Text

class ScoreDetails(BaseModel):
    accuracy: Optional[int] = None
    efficiency: Optional[int] = None
    readability: Optional[int] = None
    pep8_compliance: Optional[int] = None
    modularity_reusability: Optional[int] = None
    exception_handling: Optional[int] = None

class FeedbackDetails(BaseModel):
    accuracy: Optional[str] = None
    efficiency: Optional[str] = None
    readability: Optional[str] = None
    pep8_compliance: Optional[str] = None
    modularity_reusability: Optional[str] = None
    exception_handling: Optional[str] = None

class GradeQuizResponse(BaseModel):
    id: int
    score: ScoreDetails
    total_score: int
    summary: str
    detailed_feedback: FeedbackDetails
    positive_feedback: str
    suggestions: List[str]
    best_practice_code: str
    best_practice_explanation: str
    user_input_code: Optional[str] = None
