from fastapi import APIRouter, Security, Depends, HTTPException
from typing import Union
from sqlalchemy.orm import Session
from ..internal import schemas, crud
from ..internal.database import HTTPObjectNotFound
from ..internal.auth import AuthUser, auth
import uuid
import time

router = APIRouter(prefix='/posts')

@router.get('/all', response_model=list[schemas.Post])
def get_posts(course_code: str = "", offset: int = 0, size: int = 20, auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    """
    Gets posts w.r.t. offset and size. Hint or refine search w.r.t. course_code
    """
    return crud.get_posts(db, auth_result.uid, offset, size, course_code)

@router.get('/courses', response_model=schemas.CourseResponse)
def get_courses(filter: str | None = None, auth_result: AuthUser = Security(auth.verify, scopes=[])):
    """
    Gets a list of courses from the UW API
    """
    return crud.get_courses(filter)

@router.post('/accept/{post_id}', response_model=schemas.Chat)
def accept_post(post_id: uuid.UUID, auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    """
    This is the result of accepting a Post
    Add you to the chat if it exists OR 
    """
    return crud.accept_post(db, auth_result.uid, post_id)

@router.get('/{post_id}', response_model=schemas.Post)
def get_post(post_id: uuid.UUID, auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    # Want to verify the ownership of a post as well
    user_id = auth_result.uid
    
    item = crud.get_post(db, post_id)
    
    if not item or item.user_id != user_id: raise HTTPObjectNotFound
    
    return item
    
@router.post('', response_model=Union[schemas.Post, schemas.Chat])
def create_post(payload: schemas.CreatePost, auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    """
    First check if a post exists with similar paramters, if there is a similar one then match and create a Chat.
    
    Case 1: Does not exist post => create a new Post
    Case 2: Post exists, then accept
    """
    
    # Search similar contents
    post = crud.search_similar_post(db, auth_result.uid, payload)
    
    if post:
        # Similar contents exist, want to accept
        return crud.accept_post(db, auth_result.uid, post=post)
    else:
        epoch = int(time.time())
        user_id = auth_result.uid
        id = uuid.uuid4()
        
        post = schemas.Post(**payload.model_dump(), post_date=epoch, user_id=user_id, id=id)

        return crud.create_post(db, post)

    
@router.delete('/{post_id}', response_model=schemas.User)
def delete_post(post_id: uuid.UUID, auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    crud.delete_post(db, post_id, auth_result.uid)
    
    return crud.get_user(db, auth_result.uid)

@router.patch('/{post_id}')
def update_post(updated_post: schemas.CreatePost, post_id: uuid.UUID, auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    """
    We will only update a post if there are no chats associated with it. That is, no one has accepted it yet.
    """
    return crud.update_post(db, auth_result.uid, post_id, updated_post)



    