import httpx

from core.config import env_vars

TOKEN_URL=env_vars.TOKEN_URL
AWS_COGNITO_APP_CLIENT_ID=env_vars.AWS_COGNITO_APP_CLIENT_ID
OIDC_KAKAO_CLIENT_SECRET=env_vars.OIDC_KAKAO_CLIENT_SECRET
REDIRECT_URI=env_vars.REDIRECT_URI


async def exchange_code_for_tokens(code: str) -> dict:
    token_url = TOKEN_URL
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            token_url,
            data={
                "grant_type": "authorization_code",
                "client_id": AWS_COGNITO_APP_CLIENT_ID,
                "client_secret": OIDC_KAKAO_CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
    tokens = token_response.json()

    id_token = tokens.get("id_token")
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    return {
        "id_token": id_token, 
        "access_token": access_token, 
        "refresh_token": refresh_token
    }