"""Settings configuration."""
import secrets

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Default Settings class."""

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PROJECT_NAME: str
    HAM_QTH_USERNAME: str
    HAM_QTH_PASSWORD: SecretStr


settings = Settings()
