from pydantic import BaseModel


class GetProfile(BaseModel):
    email: str
    name: str
    language: str