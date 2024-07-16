from fastapi import Cookie, Depends, HTTPException, Request, WebSocket, WebSocketException, status
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


async def get_current_user_ws(
    websocket: WebSocket,
    cognito: AWSCognito = Depends(get_aws_cognito)
):
    access_token = websocket.cookies.get("access_token")
    
    if not access_token:
        print("No access token found")
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    
    try:
        user_details = AuthService.verify_cognito_token(access_token, cognito)

        email = next((item['Value'] for item in user_details if item['Name'] == 'email'), None)
        name = next((item['Value'] for item in user_details if item['Name'] == 'name'), None)

        user_info = {
            'email': email,
            'name': name
        }

        return user_info
    except Exception:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
