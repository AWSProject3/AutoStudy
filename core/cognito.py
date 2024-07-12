import boto3
from pydantic import EmailStr

from models.user import UserSignin, UserVerify
from core.config import env_vars

REGION = env_vars.REGION
AWS_COGNITO_APP_CLIENT_ID = env_vars.AWS_COGNITO_APP_CLIENT_ID
AWS_COGNITO_USER_POOL_ID = env_vars.AWS_COGNITO_USER_POOL_ID

class AWSCognito:
    def __init__(self):
        self.client = boto3.client("cognito-idp", region_name=REGION)

    def verify_token(self, token: str):
        response = self.client.get_user(
            AccessToken=token
        )
        return response

    def verify_account(self, data: UserVerify):
        response = self.client.confirm_sign_up(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=data.email,
            ConfirmationCode=data.confirmation_code,
        )

        return response

    def resend_confirmation_code(self, email: EmailStr):
        response = self.client.resend_confirmation_code(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=email
        )

        return response

    def user_signin(self, data: UserSignin):
        response = self.client.initiate_auth(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': data.email,
                'PASSWORD': data.password
            }
        )

        return response

    def new_access_token(self, refresh_token: str):
        response = self.client.initiate_auth(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': refresh_token,
            }
        )

        return response

    def logout(self, access_token: str):
        response = self.client.global_sign_out(
            AccessToken = access_token
        )

        return response
