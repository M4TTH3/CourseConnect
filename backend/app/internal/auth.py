from .settings import get_settings, AppSettings
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer
import jwt
import requests as req
import uuid

import hashlib

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
    uid: uuid.UUID
    sub: str
    openid: dict | None 
    hashed_open_id: dict[str, str | bytes] 
    
    def __init__(self, access_token, decoded) -> None:
        self.access_token = access_token
        self.decoded = decoded
        self.openid = None
        self.hashed_open_id = {}
        
        try:
            # uid comes as 21 digit number. lets make it a 32 bit number.
            # take the last 31 bits
            self.uid = uuid.UUID(decoded['uid'])
            self.sub = decoded['sub']
        
        except ValueError:
            raise UnauthorizedException('Bad UUID value')
        except Exception:
            raise UnauthorizedException('Missing uid or sub')
    
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
                self.openid = data.json()
                return self.openid
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
        
        if option in self.decoded:
            ret: str = self.decoded[option]
        
        elif not self.openid:
            self.get_openid()
            ret: str = self.openid.get(option)
            
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

    config: AppSettings

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
        
        if token is None: raise UnauthenticatedException()
        
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
            
            is_verified: bool | None = payload.get('is_verified')
            if not is_verified: raise UnauthorizedException('Email is not verified')
        
        except UnauthorizedException:
            raise
        
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
        
auth = VerifyJWT()