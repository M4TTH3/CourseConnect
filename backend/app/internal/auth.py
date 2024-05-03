from functools import lru_cache
from pydantic_settings import BaseSettings

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer
import jwt
import requests as req

import hashlib

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

class AuthUser:
    """
    This class will be returned to allow holds all the data for an authenticated user
    hashed_open_id stores any results of get_openid_param when hash is true
    """
    
    access_token: str
    decoded: dict[str, any]
    open_id: dict | None 
    hashed_open_id: dict[str, str | bytes] 
    
    def __init__(self, access_token, decoded) -> None:
        self.access_token = access_token
        self.decoded = decoded
        self.open_id = None
        self.hashed_open_id = {}
    
    def get_openid(self) -> dict:
        scope: str = self.decoded.get("scope")
        
        if not scope or "openid" not in scope.split(' '):
            raise 'Missing openid scope'
        
        try:
            data = req.get(
                url="https://dev-ci0ohe1d547k4xmv.us.auth0.com/userinfo",
                headers={
                    "Authorization": f'Bearer {self.access_token}'
                } 
            )
            
            if data.status_code == 200:
                self.open_id = data.json()
                return self.open_id
            else:
                raise "Bad openid retrieval"
            
        except Exception as e:
            raise UnauthorizedException(str(e))
        
    def get_openid_param(self, option: str = 'email', hash: bool = True) -> str:
        """
        Options include 'email' (only email for now)
        Will hash if is true for a protected database
        Use a faster hash sha256
        """
        
        if not self.open_id:
            self.get_openid()
    
        ret: str = self.open_id.get(option)
        if not ret: raise UnauthorizedException(f'Missing "{option} scope"')
        
        if hash:
            encoded = ret.encode('utf-8')
            ret = hashlib.sha256(encoded).hexdigest()
            self.hashed_open_id[option] = ret
        
        return ret
    
    def __str__(self) -> str:
        return f'{self.decoded}'


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
        """
        Returns:
        
        {
            access_token: str - the raw token 
            decoded: dict - the decoded token
        }
        """
        
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
        
        return AuthUser(token.credentials, payload)
    
    def _check_scopes(self, payload: dict[str, str], expected_scopes: list) -> None:
        if 'scope' not in payload:
            raise UnauthorizedException(detail="No scopes claim found in the token")
        
        scopes = payload['scope'].split(' ')
        # O(n^2) fast for small scope parameters
        for search in expected_scopes:
             if search not in scopes:
                 raise UnauthorizedException(detail=f'Missing "{search}" scope')
        
        