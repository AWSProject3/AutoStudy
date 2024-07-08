from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    REGION: str
    AWS_COGNITO_APP_CLIENT_ID: str
    AWS_COGNITO_USER_POOL_ID: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_ACCESS_KEY: str
    DATABASE_URL: str
    DB_HOST: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_PORT: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

@lru_cache
def get_settings():
    return settings

env_vars = get_settings()
