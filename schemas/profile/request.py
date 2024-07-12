from pydantic import BaseModel


class CreateProfileRequest(BaseModel):
    language: str