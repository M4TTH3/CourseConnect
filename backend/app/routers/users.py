from fastapi import APIRouter, Security
from ..internal.auth import AuthUser
from ..main import auth

router = APIRouter(prefix='/users')

@router.post('/me')
def create_user(auth_result: AuthUser = Security(auth.verify, scopes=['write:profile'])):
    return str(auth_result)