from functools import lru_cache
from pydantic_settings import BaseSettings

"""
Load the auth0 settings from .env
"""

class AppSettings(BaseSettings):
    domain: str
    api_audience: str
    issuer: str
    algorithm: str
    SQLALCHEMY_DATABASE_URL: str
    
    management_client_id: str
    management_client_secret: str
    management_aud: str
    management_token_endpoint: str
    
    class Config:
        env_file = "app/.env"

# Cache the setting to reduce reloading settings
@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()