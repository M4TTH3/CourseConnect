from fastapi import APIRouter, Security, Depends, HTTPException
from sqlalchemy.orm import Session
from ..internal import schemas, crud
from ..internal.database import HTTPObjectNotFound
from ..internal.auth import AuthUser, auth
import uuid
import time

router = APIRouter(prefix='/posts')

@router.get('/{post_id}', response_model=schemas.Post)
def get_post(post_id: uuid.UUID, auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    # Want to verify the ownership of a post as well
    user_id = auth_result.uid
    
    item = crud.get_post(db, post_id)
    
    if not item or item.user_id != user_id: raise HTTPObjectNotFound
    
    return item
    
@router.post('', response_model=schemas.Post)
def get_post(payload: schemas.CreatePost, auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    epoch = int(time.time())
    user_id = auth_result.uid
    id = uuid.uuid4()
    
    post = schemas.Post(**payload.model_dump(), post_date=epoch, user_id=user_id, id=id)

    return crud.create_post(db, post)
    
    
@router.delete('/{post_id}', status_code=204)
def get_post(post_id: uuid.UUID, auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    crud.delete_post(db, post_id, auth_result.uid)
    
    return "Successfully deleted"


@router.post('/accept/{post_id}')
def accept_post(auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    """
    This is the result of accepting a 
    """
    
    pass
    