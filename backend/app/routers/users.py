from fastapi import APIRouter, Security, Depends, HTTPException
from sqlalchemy.orm import Session
from ..internal import schemas, crud
from ..internal.database import HTTPObjectNotFound
from ..internal.auth import AuthUser, auth
from app.internal.management import get_access_token
import requests as req

router = APIRouter(prefix='/users')

@router.get('/me', response_model=schemas.User)
def get_user(auth_result: AuthUser = Security(auth.verify, scopes=['read:profile']), db: Session = Depends(crud.get_db)):
    id = auth_result.uid
    user = crud.get_user(db, id)
    
    if not user: raise HTTPObjectNotFound()
    return user
    

@router.post('/me', response_model=schemas.User)
def create_user(auth_result: AuthUser = Security(auth.verify, scopes=['write:profile']), db: Session = Depends(crud.get_db)):
    """
    Will create a user, but first enforce that the user isn't created already.
    
    """
    id = auth_result.uid
    user = schemas.User(id=id)
    
    return crud.create_user(db, user)

@router.delete('/me', status_code=204)
def delete_user(auth_result: AuthUser = Security(auth.verify, scopes=['write:profile']), db: Session = Depends(crud.get_db)):
    """
    First delete user from database
    Then delete from AUTH0
    """
    id = auth_result.uid
    sub = auth_result.sub
    
    # Delete from DB
    crud.delete_user(db, id)
    
    # Delete from Auth0
    access_token, endpoint = get_access_token()
    request = req.delete(f'{endpoint}users/{sub}', headers={
        'Authorization': f'Bearer {access_token}'
    })

    if request.status_code != 204: raise HTTPException(request.status_code, request.reason)
    
    return "Successfully deleted haha"
    
    