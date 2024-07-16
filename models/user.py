from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, Field

class UserContext(BaseModel):
    email: str
    name: str

    @classmethod
    def from_dict(cls, user_dict: dict):
        return cls(email=user_dict['email'], name=user_dict['name'])

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


class ConfirmForgotPassword(BaseModel):
    email: EmailStr
    confirmation_code: Annotated[str, MaxLen(6)]
    new_password: Annotated[str, MinLen(8)]


class ChangePassword(BaseModel):
    old_password: Annotated[str, MinLen(8)]
    new_password: Annotated[str, MinLen(8)]
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str