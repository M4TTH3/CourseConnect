from sqlalchemy.orm import Session
from . import schemas, db_models as models
from .database import HTTPObjectExists, engine, SessionLocal, HTTPObjectNotFound
from fastapi import HTTPException
from typing import Generator
from uuid import UUID

models.DB_Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Yield a database session and enforce it closes w.r.t. FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
Create Read Update Delete (CRUD)
"""


"""
User Functions
"""

def delete_user(db: Session, id: UUID) -> bool:
    user: schemas.User = get_user(db, id)
    if not user: return False
    
    db.delete(user)
    db.commit()
    
    return True

def get_user(db: Session, id: UUID) -> models.User | None:
    return db.query(models.User).filter(models.User.id == id).first()

def create_user(db: Session, user: schemas.User) -> models.User:
    # First ensure the user hasn't been created already
    if get_user(db, user.id): raise HTTPObjectExists()
    
    db_item = models.User(**user.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item
    
"""
Post Functions
"""

def get_post(db: Session, id: UUID) -> models.Post | None:
    return db.query(models.Post).filter(models.Post.id == id).first()

def create_post(db: Session, post: schemas.Post) -> models.Post:
    
    if get_post(db, post.id): raise HTTPObjectExists()
    
    db_item = models.Post(**post.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item

def delete_post(db: Session, post_id: UUID, user_id: UUID) -> bool:
    post = get_post(db, post_id)
    
    if post.user_id != user_id: raise HTTPException(400, "User does not own post")
    
    if not post: raise HTTPObjectNotFound()
    
    db.delete(post)
    db.commit()
    
    return True
