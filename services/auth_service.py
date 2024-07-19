from fastapi import HTTPException, Response
from fastapi.responses import JSONResponse
import botocore
from pydantic import EmailStr
from starlette.status import HTTP_307_TEMPORARY_REDIRECT

from core.cognito import AWSCognito
from core.config import env_vars
from models.user import UserSignin, UserVerify
import security

FRONT_URL = env_vars.FRONT_URL

class AuthService:
    async def exchange_code_for_tokens(code: str, response: Response) -> str:
        try:
            tokens: dict = await security.exchange_code_for_tokens(code)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
        
        else:
            response = Response(status_code=HTTP_307_TEMPORARY_REDIRECT)
            response.headers["Location"] = f"{FRONT_URL}/callback"
            
            response.set_cookie(key="access_token", value=tokens['access_token'], httponly=True, secure=True, samesite='None', path="/")
            response.set_cookie(key="refresh_token", value=tokens['refresh_token'], httponly=True, secure=True, samesite='None', path="/")
            response.set_cookie(key="id_token", value=tokens['id_token'], httponly=True, secure=True, samesite='None', path="/")
            return response
        
    def verify_cognito_token(access_token: str, cognito: AWSCognito):
        try:
            response = cognito.verify_token(access_token)
            user_info = response["UserAttributes"]

        except botocore.exceptions.ClientError as e:
            raise HTTPException(status_code=401, detail="Invalid token")
        else:
            return user_info

    def verify_account(data: UserVerify, cognito: AWSCognito):
        try:
            response = cognito.verify_account(data)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'CodeMismatchException':
                raise HTTPException(
                    status_code=400, detail="The provided code does not match the expected value.")
            elif e.response['Error']['Code'] == 'ExpiredCodeException':
                raise HTTPException(
                    status_code=400, detail="The provided code has expired.")
            elif e.response['Error']['Code'] == 'UserNotFoundException':
                raise HTTPException(
                    status_code=404, detail="User not found")
            elif e.response['Error']['Code'] == 'NotAuthorizedException':
                raise HTTPException(
                    status_code=200, detail="User already verified.")
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            return JSONResponse(content={"message": "Account verification successful"}, status_code=200)
        
    def resend_confirmation_code(email: EmailStr, cognito: AWSCognito):
        try:
            response = cognito.check_user_exists(email)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'UserNotFoundException':
                raise HTTPException(
                    status_code=404, detail="User deos not exist")
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            try:
                response = cognito.resend_confirmation_code(email)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'UserNotFoundException':
                    raise HTTPException(
                        status_code=404, detail="User not found")
                elif e.response['Error']['Code'] == 'LimitExceededException':
                    raise HTTPException(
                        status_code=429, details="Limit exceeded")
                else:
                    raise HTTPException(
                        status_code=500, detail="Internal Server")
            else:
                return JSONResponse(content={"message": "Confirmation code sent successfully"}, status_code=200)
            
    def user_signin(data: UserSignin, cognito: AWSCognito):
        try:
            response = cognito.user_signin(data)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'UserNotFoundException':
                raise HTTPException(
                    status_code=404, detail="User deos not exist")
            elif e.response['Error']['Code'] == 'UserNotConfirmedException':
                raise HTTPException(
                    status_code=403, detail="Please verify your account")
            elif e.response['Error']['Code'] == 'NotAuthorizedException':
                raise HTTPException(
                    status_code=401, detail="Incorrect username or password")
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            content = {
                "message": 'User signed in successfully',
                "AccessToken": response['AuthenticationResult']['AccessToken'],
                "RefreshToken": response['AuthenticationResult']['RefreshToken']
            }
            return JSONResponse(content=content, status_code=200)

    def new_access_token(refresh_token: str, cognito: AWSCognito):
        try:
            response = cognito.new_access_token(refresh_token)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'InvalidParameterException':
                raise HTTPException(
                    status_code=400, detail="Refresh token provided has wrong format")
            elif e.response['Error']['Code'] == 'NotAuthorizedException':
                raise HTTPException(
                    status_code=401, detail="Invalid refresh token provided")
            elif e.response['Error']['Code'] == 'LimitExceededException':
                raise HTTPException(
                    status_code=429, detail="Attempt limit exceeded, please try again later")
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            content = {
                "message": 'Refresh token generated successfully',
                "AccessToken": response['AuthenticationResult']['AccessToken'],
                "ExpiresIn": response['AuthenticationResult']['ExpiresIn'],
            }
            return JSONResponse(content=content, status_code=200)

    def logout(access_token: str, cognito: AWSCognito, response: Response):
        try:
            cognito_response = cognito.logout(access_token)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'InvalidParameterException':
                raise HTTPException(
                    status_code=400, detail="Access token provided has wrong format")
            elif e.response['Error']['Code'] == 'NotAuthorizedException':
                raise HTTPException(
                    status_code=401, detail="Invalid access token provided")
            elif e.response['Error']['Code'] == 'TooManyRequestsException':
                raise HTTPException(
                    status_code=429, detail="Too many requests")
            else:
                raise HTTPException(status_code=500, detail="Internal Server")
        else:
            response.delete_cookie("access_token", domain="localhost", path="/", secure=True, httponly=True, samesite='lax')
            response.delete_cookie("refresh_token", domain="localhost", path="/", secure=True, httponly=True, samesite='lax')
            response.delete_cookie("id_token", domain="localhost", path="/", secure=True, httponly=True, samesite='lax')

            return JSONResponse(content={"message": "Logged out successfully"})


