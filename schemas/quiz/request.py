from pydantic import BaseModel, field_validator

class GenerateQuizRequest(BaseModel):
    source_language: str
    target_language: str
    difficulty: str
    # category: str = None

class GradeQuizRequest(BaseModel):
    id: int
    source_language: str
    target_language: str
    difficulty: str
    quiz: str
    user_input_code: str


