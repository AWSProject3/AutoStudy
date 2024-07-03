from pydantic import BaseModel, field_validator

class GenerateQuizRequest(BaseModel):
    source_language: str
    target_language: str
    difficulty: str
    # category: str = None

    # @field_validator("source_lang", "target_lang", "difficulty")
    # def not_empty(cls, value):
    #     if not value:
    #         raise ValueError("must not be empty")
    #     return value
    


