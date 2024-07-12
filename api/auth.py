from typing import Optional

from fastapi import APIRouter, Cookie, Response, status, Depends
from fastapi import Request

from models.user import RefreshToken, UserSignin, UserVerify
from services.auth_service import AuthService
from core.cognito import AWSCognito
from core.dependencies import get_aws_cognito


router = APIRouter(prefix='/api/auth')

@router.get("/callback")
async def callback(request: Request, response: Response):
    return await AuthService.exchange_code_for_tokens(request.query_params.get("code"), response)

# verify account
@router.post('/verify_account', status_code=status.HTTP_200_OK, tags=["Auth"])
async def verify_account(
    data: UserVerify,
    cognito: AWSCognito = Depends(get_aws_cognito),
):
    return AuthService.verify_account(data, cognito)


# resend confirmation code
@router.post('/resend_confirmation_code', status_code=status.HTTP_200_OK, tags=['Auth'])
async def resend_confirmation_code(email_data: str, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.resend_confirmation_code(email_data.email, cognito)


# sign in
@router.post('/signin', status_code=status.HTTP_200_OK, tags=["Auth"])
async def signin(data: UserSignin, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.user_signin(data, cognito)


# generate new token
@router.post('/new_token', status_code=status.HTTP_200_OK, tags=["Auth"])
async def new_access_token(refresh_token: RefreshToken, cognito: AWSCognito = Depends(get_aws_cognito)):
    return AuthService.new_access_token(refresh_token.refresh_token, cognito)


# logout
@router.post('/logout', status_code=status.HTTP_200_OK, tags=["Auth"])
async def logout(
    response: Response,
    access_token: Optional[str] = Cookie(None),
    cognito: AWSCognito = Depends(get_aws_cognito),
):
    return AuthService.logout(access_token, cognito, response)


# get user detail by access_token
@router.get('/user_details_by_token', status_code=status.HTTP_200_OK, tags=["Auth"])
async def user_details_by_token(
    access_token: Optional[str] = Cookie(None),
    cognito: AWSCognito = Depends(get_aws_cognito)
):
    return AuthService.verify_cognito_token(access_token, cognito)
