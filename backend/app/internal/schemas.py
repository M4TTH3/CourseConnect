from typing import Any
from pydantic import BaseModel
from uuid import UUID

"""
Schemas are used to precisely define how python can interact with db_models
"""


"""
Define the User Schemas
"""

class UserBase(BaseModel):
    id: UUID

class CreateUser(UserBase):
    pass

class User(UserBase):
    blocked: list[str] = []
    reports: list[str] = []

    posts: list['Post'] = []
    chats: list['Chat'] = []
    
    class Config:
        from_attributes = True
    

"""
Define the Chat Schemas
"""

class ChatBase(BaseModel):
    id: UUID
    
class Chat(ChatBase):
    post_date: int
    course: str
    content_type: str
    content_number: int | None = None
    
    users: list['UserBase'] # Want only IDs from User
    messages: list['Message'] = []
    
    def model_post_init(self, __context: Any) -> None:
        """
        Want to hide extra data if provided User
        """
        self.users = [UserBase(**test.model_dump()) for test in self.users]
    
    class Config:
        from_attributes = True


"""
Define the Message Schema
"""

class MessageBase(BaseModel):
    pass
    
class CreateMessage(MessageBase):
    contents: str
    chat_id: UUID
    
class Message(CreateMessage):
    sender: str
    id: UUID

    class Config:
        orm_mode = True

"""
Define the Post Schemas
"""

class PostBase(BaseModel):
    pass
    
class CreatePost(PostBase):
    """
    course: the course the post refers to
    content_type: Assignment | Quiz | Midterm | Final
    content_number: Specify Selection
    """
    size_limit: int
    course_code: str
    content_type: str
    content_number: int | None = None
    description: str
    
class Post(CreatePost):
    """
    course: the course the post refers to
    content_type: Assignment | Quiz | Midterm | Final
    content_number: Specify Selection
    """
    id: UUID
    post_date: int
    user_id: UUID
    
    # Commented because no need to track user
    # user: 'User'
    
    class Config:
        from_attributes = True
        


    