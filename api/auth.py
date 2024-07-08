from fastapi import APIRouter, status, Depends
from pydantic import EmailStr

from models.user import AccessToken, ChangePassword, ConfirmForgotPassword, RefreshToken, UserSignin, UserSignup, UserVerify
from services.auth_service import AuthService
from core.cognito import AWSCognito
from core.dependencies import get_aws_cognito

router = APIRouter(prefix='/api/auth')

# sign up
@router.post('/signup', status_code=status.HTTP_201_CREATED, tags=['Auth'])
async def signup_user(user: UserSignup, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.user_signup(user, cognito)

# verify account
@router.post('/verify_account', status_code=status.HTTP_200_OK, tags=["Auth"])
async def verify_account(
    data: UserVerify,
    cognito: AWSCognito = Depends(get_aws_cognito),
):
    return AuthService.verify_account(data, cognito)


# resend confirmation code
@router.post('/resend_confirmation_code', status_code=status.HTTP_200_OK, tags=['Auth'])
async def resend_confirmation_code(email: EmailStr, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.resend_confirmation_code(email, cognito)


# sign in
@router.post('/signin', status_code=status.HTTP_200_OK, tags=["Auth"])
async def signin(data: UserSignin, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.user_signin(data, cognito)

# forgot password
@router.post('/forgot_password', status_code=status.HTTP_200_OK, tags=["Auth"])
async def forgot_password(email: EmailStr, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.forgot_password(email, cognito)


# confirm forgot password
@router.post('/confirm_forgot_password', status_code=status.HTTP_200_OK, tags=["Auth"])
async def confirm_forgot_password(data: ConfirmForgotPassword, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.confirm_forgot_password(data, cognito)


# change password
@router.post('/change_password', status_code=status.HTTP_200_OK, tags=["Auth"])
async def change_password(data: ChangePassword, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.change_password(data, cognito)


# generate new token
@router.post('/new_token', status_code=status.HTTP_200_OK, tags=["Auth"])
async def new_access_token(refresh_token: RefreshToken, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.new_access_token(refresh_token.refresh_token, cognito)


# logout
@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT, tags=["Auth"])
async def logout(access_token: AccessToken, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.logout(access_token.access_token, cognito)


# get user detail
@router.get('/user_details', status_code=status.HTTP_200_OK, tags=["Auth"])
async def user_details(email: EmailStr, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.user_details(email, cognito)
