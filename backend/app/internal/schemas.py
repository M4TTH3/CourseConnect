from typing import Any, Literal
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
    size_limit: int
    course_code: str
    content_type: str
    content_number: int | None = None
    post_id: UUID | None = None
    users: list['UserBase'] = [] # Want only IDs from User
    
    # Don't need the post attribute
    def model_post_init(self, __context: Any) -> None:
        """
        Want to hide extra data if provided User
        """
        self.users = [UserBase(**test.model_dump()) for test in self.users]
    
    
class Chat(ChatSimplfiied):

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
    sender: UUID
    post_date: int
    
class Message(CreateMessage):
    id: int

    class Config:
        from_attributes = True

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
        
        
"""
Formatting Responses and Payloads in the chat websocket
"""

class ChatAction(BaseModel):
    """
    This will be the default template for receiving via websocket
    
    Action has types:
    - send (sends a message)
    - delete (deletes a message)
    - scroll (increments pagesize and returns a list of messages of size pagesize)
    """
    
    action: Literal['send', 'delete', 'scroll']
    payload: str | int | None = None

class ChatResponse(BaseModel):
    """
    Action has types:
    - update_last (update the last message in the list)
    - refresh (update all messages on front end)
    - delete (given an integer ID for the message to remove)
    - error
    """
    
    action: Literal['update_last', 'refresh', 'delete', 'error']
    payload: Message | list[Message] | int | str
    

"""
Response for UW API Courses 
"""
class Course(BaseModel):
    course_code: str
    course_name: str
    description: str

class CourseResponse(BaseModel):
    courses: list[Course]
