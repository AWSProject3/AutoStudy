from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field

class UserSignup(BaseModel):
    name: str = Field(max_length=50)
    email: EmailStr
    password: Annotated[str, MinLen(8)]
    language: str

class UserVerify(BaseModel):
    email: EmailStr
    confirmation_code: Annotated[str, MaxLen(6)]

class UserSignin(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8)]
