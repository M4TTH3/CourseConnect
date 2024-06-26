from sqlalchemy.orm import Session
from . import schemas, db_models as models
from .database import HTTPObjectExists, engine, SessionLocal, HTTPObjectNotFound
from fastapi import HTTPException
from typing import Generator
from uuid import UUID
from .settings import get_settings
import requests as req
import random

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

def get_posts(db: Session, id: UUID, offset: int, size: int, course_code: str) -> list[models.Post]:
    """
    Returns a list of size n of Posts that the user doesn't own.
    """
    return db.query(models.Post).filter(models.Post.user_id != id, models.Post.course_code.contains(course_code)).offset(offset).limit(size).all()

def get_post(db: Session, id: UUID) -> models.Post | None:
    return db.query(models.Post).filter(models.Post.id == id).first()

def search_similar_post(db: Session, user_id: UUID, post: schemas.CreatePost) -> models.Post | None:
    """
    This function returns any posts that have similar course_code, content_type, content_number, and size_limit
    
    Also can't be something you own
    """
    
    return db.query(models.Post).filter(
        models.Post.course_code == post.course_code,
        models.Post.content_type == post.content_type,
        models.Post.content_number == post.content_number,
        models.Post.size_limit == post.size_limit,
        models.Post.user_id != user_id
    ).first()


def create_post(db: Session, post: schemas.Post) -> models.Post:
    
    if get_post(db, post.id): raise HTTPObjectExists()
    
    db_item = models.Post(**post.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item

def delete_post(db: Session, post_id: UUID, user_id: UUID, force = False) -> bool:
    """
    If force is true, then the user does not need to own the post to delete it
    """
    post = get_post(db, post_id)
    
    if not post: raise HTTPObjectNotFound()
    if not force and post.user_id != user_id: raise HTTPException(400, "User does not own post")
    if post.linked_chat: raise HTTPException(400, "Can't delete a post that has been accepted")
    
    db.delete(post)
    db.commit()
    
    return True

def update_post(db: Session, user_id: UUID, post_id: UUID, updated_params: schemas.CreatePost) -> models.Post:
    """
    This is to update the parameters. Note if a chat exists, then we want to update it as well.
    Can only update it if there are no chats linked to it.
    """
    post = get_post(db, post_id)
    
    if not post or user_id != post.user_id: raise HTTPObjectNotFound("Post belonging to user")
    if post.linked_chat: raise HTTPException(400, "Can't update a post that has been accepted")
    
    post.course_code = updated_params.course_code
    post.content_type = updated_params.content_type
    post.content_number = updated_params.content_number
    post.description = updated_params.description
    post.size_limit = updated_params.size_limit
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return post

def accept_post(db: Session, user_id: UUID, post_id: UUID = None, post: models.Post = None) -> models.Chat | None:
    """
    post_id - find post first
    post - provide the model from the db
    
    Case 1: Exist Post AND Chat then join Chat, if Post now reach size_limit delete Post
    Case 2: Exist Post AND Chat DNE then create Chat, if Post now reach size_limit delete Post 
    """
    
    # Get the correct Post object
    if not post_id and not post: return None
    if post_id: post = get_post(db, post_id)
    
    # Check that you aren't accepting your own post
    if post.user_id == user_id: raise HTTPException(400, "Can't accept own Post")
    
    # Get the user object to attach to chat
    user = get_user(db, user_id)
    post_user = get_user(db, post.user_id)
    if not user: raise HTTPObjectNotFound("User")
    
    chat: models.Chat = post.linked_chat
    
    if not chat: 
        chat = create_chat(
            db, 
            schemas.Chat(
                id=post.id, 
                size_limit=post.size_limit, 
                course_code=post.course_code, 
                content_type=post.content_type, 
                content_number=post.content_number,
                post_id=post.id
            ),
            commit=False
        )
        
    # Add the user to chat and update the database
    chat.users.extend([user, post_user])
    db.add(chat)
    
    # Check if the chat is full now
    if len(chat.users) == post.size_limit:
        db.delete(post)
        chat.post_id = None
    
    db.commit()
    db.refresh(chat)
    
    return chat

"""
Chat Functions
"""
def get_chat(db: Session, chat_id: UUID) -> models.Chat | None:
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()

def leave_chat(db: Session, chat_id: UUID, user_id: UUID) -> models.User:
    chat_item = get_chat(db, chat_id)
    user = get_user(db, user_id)

    if not chat_item or not user: raise HTTPObjectNotFound("Chat and/or User")
    
    # Check user is inside
    if not user in chat_item.users: raise HTTPException(400, "User isn't in this chat")
    user.chats.remove(chat_item)
    db.add(user)
    
    if len(chat_item.users) == 1:
        # Delete the chat and correlated Post if applicable
        if chat_item.post:
            db.delete(chat_item.post)

        db.delete(chat_item)
    
    db.commit()
    db.refresh(user)
    
    return user


def create_chat(db: Session, chat: schemas.Chat, commit = True, *users: models.User) -> models.Chat:
    
    if get_chat(db, chat.id): raise HTTPObjectExists()
    
    db_item = models.Chat(**chat.model_dump())
    
    for user in users:
        db_item.users.append(user)
    
    db.add(db_item)
    if commit: 
        db.commit()
        db.refresh(db_item)
    
    return db_item

"""
Message CRUD operations 
"""
def get_messages(db: Session, chat_id: UUID, pagesize: int) -> list[models.Message]:
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).order_by(models.Message.post_date).limit(pagesize).all()

def create_message(db: Session, message: schemas.CreateMessage) -> models.Message:
    # The DB will autoincrement and assign the message ID
    db_item = models.Message(**message.model_dump())
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item

def delete_message(db: Session, message_id: int, sender: UUID) -> bool:
    item = db.query(models.Message).filter(models.Message.id == message_id).first()
    
    if item.sender != sender: raise HTTPException(400, "User didn't send this message")
    
    db.delete(item)
    db.commit()
    
    return True

def get_courses(filter: str | None) -> schemas.CourseResponse:
    """
    Get the courses from uwaterloo api endpoint. Need to get the term first
    """

    settings = get_settings()
    base_endpoint = "https://openapi.data.uwaterloo.ca/v3"
    current_term_endpoint = f"{base_endpoint}/Terms/current"

    response = req.get(current_term_endpoint, headers={"X-API-KEY": settings.uw_api_key})
    term = response.json()["termCode"]

    courses_endpoint = f"{base_endpoint}/Courses/{term}"
    response = req.get(courses_endpoint, headers={"X-API-KEY": settings.uw_api_key})
    courses_raw: list[dict[str, str]] = response.json()
    
    # For returning
    courses: list[schemas.Course] = []
    courses_by_desc: list[schemas.Course] = []

    # If the filter is not provided, then return a random 10 courses
    if not filter:
        max_len = len(courses_raw)
        random_incides = random.sample(range(max_len), k=min(max_len, 10))
        for course in [courses_raw[i] for i in random_incides]:
            courses.append(schemas.Course(
                course_code=f"{course['subjectCode']} {course['catalogNumber']}",
                course_name=course["title"],
                description=course["description"]
            ))
        return schemas.CourseResponse(courses=courses)
    
    # We will get the courses by code first. If it comes empty, we will use the course name
    # Make this more efficent by only querying until max of 10 items.
    # Fill array of description as a backup.
    
    # Set it to the lower case
    filter = filter.lower().replace(' ', '')
    filter_numeric = filter.isnumeric()
    filter_alpha = filter.isalpha()
    
    for course in courses_raw:
        if (len(courses)) >= 10: break
        
        if (filter_numeric and filter in course["catalogNumber"]
            or (
                not filter_numeric
                and filter_alpha
                and course["subjectCode"].startswith(filter)
            )
            or (
                not filter_numeric
                and not filter_alpha
                and filter
                in f"{course['subjectCode']}{course['catalogNumber']}".lower()
            )
        ): courses.append(schemas.Course(
            course_code=f"{course['subjectCode']} {course['catalogNumber']}",
            course_name=course["title"],
            description=course["description"]
        ))
        
        if (len(courses_by_desc) < 10 and filter in course["description"].lower()):
            courses_by_desc.append(schemas.Course(
                course_code=f"{course['subjectCode']} {course['catalogNumber']}",
                course_name=course["title"],
                description=course["description"]
            ))

    # Empty case, then go by descriptions.
    if len(courses) == 0:
        return schemas.CourseResponse(courses=courses_by_desc[0: min(len(courses_by_desc), 10)])

    # Limit the number of courses to 10
    return schemas.CourseResponse(courses=courses[0: min(len(courses), 10)])
