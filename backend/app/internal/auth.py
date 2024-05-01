from functools import lru_cache
from typing_extensions import Annotated, Doc
from pydantic_settings import BaseSettings

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer
import jwt

"""
Load the auth0 settings from .env
"""

class AUTH0_Settings(BaseSettings):
    domain: str
    api_audience: str
    issuer: str
    algorithm: str
    
    class Config:
        env_file = "app/.env"

# Cache the setting to reduce reloading settings
@lru_cache()
def get_settings() -> AUTH0_Settings:
    return AUTH0_Settings()

"""
Create the class to verify the token
"""

class UnauthorizedException(HTTPException):
    def __init__(self, detail: any = None) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)

class UnauthenticatedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail="Requires Authentication token")

class VerifyJWT:

    config: AUTH0_Settings

    def __init__(self) -> None:
        self.config = get_settings()

        # Process JWKS to use available keys
        jwks_url = f'https://{self.config.domain}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(self, security_scopes: SecurityScopes, token: HTTPAuthorizationCredentials | None = Depends(HTTPBearer())) -> dict | None:
        if token is None: raise UnauthenticatedException
        
        try:
            # Get token 'kid'
            signing_key = self.jwks_client.get_signing_key_from_jwt(token.credentials).key 
            
            # Get the payload
            payload: dict = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=self.config.algorithm,
                audience=self.config.api_audience,
                issuer=self.config.issuer
            )
            
        except Exception as error:
            raise UnauthorizedException(str(error))
        
        if len(security_scopes.scopes) > 0:
            self._check_scopes(payload, security_scopes.scopes)
        
        return payload
    
    def _check_scopes(self, payload: dict[str, str], expected_scopes: list) -> None:
        if 'scope' not in payload:
            raise UnauthorizedException(detail="No scopes claim found in the token")
        
        scopes = payload['scope'].split(' ')
        # O(n^2) fast for small scope parameters
        for search in expected_scopes:
             if search not in scopes:
                 raise UnauthorizedException(detail=f'Missing "{search}" scope')
        
        