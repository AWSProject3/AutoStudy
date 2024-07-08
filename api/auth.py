# auth_route.py
from fastapi import APIRouter, status, Depends

from models.user import UserSignup
from services.auth_service import AuthService
from core.cognito import AWSCognito
from core.dependencies import get_aws_cognito

router = APIRouter(prefix='/api/auth')

# USER SIGNUP
@router.post('/signup', status_code=status.HTTP_201_CREATED, tags=['Auth'])
async def signup_user(user: UserSignup, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.user_signup(user, cognito)

# @router.post()
# async def verify_account():

# @router.post()
# async def signin_user():

