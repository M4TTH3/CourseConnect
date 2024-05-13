"""
Models are SQLAlchemy ORM used to define Table properties
"""

from sqlalchemy import Column, ForeignKey, UUID, String, ARRAY, Table, Integer, BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from .database import DB_Base

"""
User (One to Many) Posts
User (Many to Many) Chats
Chat (One to Many) Message
"""

user_chat = Table(
    "user_chat_association_table", DB_Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("chat_id", ForeignKey("chats.id"), primary_key=True)
)

class User(DB_Base):
    """
    id: given by auth0
    
    blocked: All hashed emails the user has blocked
    reports: All reports directed at the current user
    """
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    blocked = Column(ARRAY(String))
    reports = Column(ARRAY(String))
    
    posts = relationship("Post", back_populates="user", cascade='all, delete')
    chats = relationship("Chat", secondary=user_chat, back_populates="users")
    
class Post(DB_Base):
    """
    This is a post and it will have a unique_id that will be used when converted to a Chat
    
    post_date: epoch time - Use this for deleting older posts or filtering by post_date
    course_code: str - the course they're taking i.e. CS246
    content_type: str - the type of content, Assignment | Quiz | Midterm | Final
    content_number: str - The number for the content_type like 5 for "Assignment 5"
    """
    
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    post_date = Column(BIGINT, index=True)
    course_code = Column(String, index=True)
    content_type = Column(String)
    content_number = Column(Integer, nullable=True)
    description = Column(String)
    size_limit = Column(Integer, index=True)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    user = relationship("User", back_populates="posts")
    linked_chat = relationship("Chat", back_populates="post", uselist=False)
    

class Chat(DB_Base):
    """
    This is a chat and is linked with multiple Users. It holds a log of conversations
    """
    
    __tablename__ = "chats"
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    size_limit = Column(Integer, index=True)
    course_code = Column(String, index=True)
    content_type = Column(String)
    content_number = Column(Integer, nullable=True)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=True)
    
    users = relationship("User", secondary=user_chat, back_populates="chats")
    messages = relationship("Message", back_populates="chat", cascade='all, delete')
    post = relationship("Post", back_populates="linked_chat")
    
    
class Message(DB_Base):
    """
    This is a message and is linked with a specific Chat.
    sender: str - the ID of the sender
    contents: str - the contents of the message
    chat_id: Integer (the ID of chat it belongs to)
    """
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(UUID(as_uuid=True), index=True)
    contents = Column(String)
    post_date = Column(BIGINT, index=True)
    chat_id = Column(UUID(as_uuid=True), ForeignKey("chats.id"))

    chat = relationship("Chat", back_populates="messages")
    
    
    
    
