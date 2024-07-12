from fastapi import Depends, HTTPException, Request
from core.cognito import AWSCognito

from services.auth_service import AuthService

def get_aws_cognito() -> AWSCognito:
    return AWSCognito()


def get_current_user(
    request: Request,
    cognito: AWSCognito = Depends(get_aws_cognito)
):
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_details = AuthService.verify_cognito_token(access_token, cognito)

    email = next((item['Value'] for item in user_details if item['Name'] == 'email'), None)
    name = next((item['Value'] for item in user_details if item['Name'] == 'name'), None)

    user_info = {
        'email': email,
        'name': name
    }

    return user_info

