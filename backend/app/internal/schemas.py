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
    
    def model_post_init(self, __context: Any) -> None:
        """
        Hide any posts that have become a chat already
        """
        self.posts = [post for post in self.posts if not post.linked_chat]
    
    class Config:
        from_attributes = True
    

"""
Define the Chat Schemas
"""

class ChatBase(BaseModel):
    id: UUID
    
class ChatSimplfiied(ChatBase):
    """
    This one will restrict access to seeing messages from the Chats.
    Used for querying public Posts and hiding the associated messages
    """
    users: list['UserBase'] = [] # Want only IDs from User
    
    # Don't need the post attribute
    def model_post_init(self, __context: Any) -> None:
        """
        Want to hide extra data if provided User
        """
        self.users = [UserBase(**test.model_dump()) for test in self.users]
    
class Chat(ChatSimplfiied):

    size_limit: int
    course_code: str
    content_type: str
    content_number: int | None = None
    post_id: UUID | None = None
    
    users: list['UserBase'] = [] 
    messages: list['Message'] = []
    
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
    
    If linked_chat is None, then you can edit your post
    Otherwise can't edit
    """
    id: UUID
    post_date: int
    user_id: UUID
    
    linked_chat: ChatSimplfiied | None = None
    
    # Commented because no need to track user
    # user: 'User'
    
    def model_post_init(self, __context: Any) -> None:
        """
        Ensure it's type ChatSimplified to hide messages
        """
        if self.linked_chat: self.linked_chat = ChatSimplfiied(**self.linked_chat.model_dump())
    
    class Config:
        from_attributes = True
        


    