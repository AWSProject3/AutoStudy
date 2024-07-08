import boto3

from models.user import UserSignup
from core.config import env_vars

REGION = env_vars.REGION
AWS_COGNITO_APP_CLIENT_ID = env_vars.AWS_COGNITO_APP_CLIENT_ID
AWS_COGNITO_USER_POOL_ID = env_vars.AWS_COGNITO_USER_POOL_ID

class AWSCognito:
    def __init__(self):
        self.client = boto3.client("cognito-idp", region_name=REGION)

    def user_signup(self, user: UserSignup):
        response = self.client.sign_up(
            ClientId=AWS_COGNITO_APP_CLIENT_ID,
            Username=user.email,
            Password=user.password,
            UserAttributes=[
                {
                    'Name': 'name',
                    'Value': user.name,
                },
                {
                    'Name': 'custom:language',
                    'Value': user.language
                }
            ],
        )

        return response

    # def verify_account():

    # def user_signin():
    #...
