from fastapi import (
    WebSocket,
    HTTPException
)
from . import db_models as models, schemas, crud
from sqlalchemy.orm import Session
import uuid, time


class GroupMember(WebSocket):
    """
    This class will hold the members' websocket, pagesize (number of messages required), and ID
    """
    pagesize: int
    id: uuid.UUID
    
    def __init__(self, ws: WebSocket, id: uuid.UUID) -> None:
        self.id = id
        self.pagesize = 0 # Start with 0 messages and then on first scroll we update
        super.__init__(ws)
        
    def update_pagesize(self, increment = 25) -> None:
        """
        When a user wants to scroll up, increment the number of messages to receive
        """
        self.pagesize += increment
        

class GroupSession:
    """
        Make the members an array object to reduce space allocation. Members <= 4
        
        id_code: uniquely defines the group session
        members: holds connection for all connected members
        max_pagesize: the largest offset of all the members, defaults 20
    """

    chat_id: uuid.UUID
    members: list[GroupMember]

    def __init__(self, chat_id: uuid.UUID) -> None:
        self.chat_id = chat_id
        self.members = []

    def attach(self, member: GroupMember) -> None:
        if member in self.members: raise HTTPException(status_code=400, detail="User already connected")
        if len(self.members) == 4: raise HTTPException(status_code=400, detail="Group full already")
        
        self.members.append(member)

    def disconnect(self, member: GroupMember) -> None:
        try:
            self.members.remove(member)
        except ValueError:
            raise HTTPException(status_code=400, detail="Member not connected in the chat")

    async def send(self, msg: str, sender: uuid.UUID, db: Session) -> None:
        "Sends the message to everyone in the group"
        # First upload into the DB
        send = schemas.CreateMessage(contents=msg, chat_id=self.chat_id, sender=sender, post_date=time.time())
        item = crud.create_message(db, send)
        
        payload = schemas.Message.model_validate(item)
        response = schemas.ChatResponse(action="update_last", payload=payload)
        
        # Now send the response to every user in the session
        for member in self.members:
            await member.send_json(response.model_dump())
        
    async def scroll(self, member: GroupMember, db: Session) -> None:
        """
        We want to scroll up and load more messages
        """
        member.update_pagesize()
        messages = crud.get_messages(db, self.chat_id, member.pagesize)
        payload = [schemas.Message.model_validate(msg) for msg in messages]
        response = schemas.ChatResponse(action='refresh', payload=payload)
        
        await member.send_json(response.model_dump())
        
    async def delete_message(self, message_id: int, user_id: uuid.UUID, db: Session):
        """
        Delete the message and update that to all the users
        """
        if not crud.delete_message(db, message_id, user_id): raise HTTPException(400, "bad request")
        
        response = schemas.ChatResponse(action='delete', payload=message_id)
        
        for member in self.members:
            await member.send_json(response.model_dump()) 
    
    def __len__(self) -> int:
        return len(self.members)


class GroupSessionsManager:
    """
        Manages all the different group sessions happening at the same time
    """

    sessions: dict[uuid.UUID, GroupSession]

    def __init__(self) -> None:
        self.sessions = {}

    def attach(self, chat_id: uuid.UUID, member: GroupMember) -> None:
        session = self.sessions.get(chat_id)

        if not session: 
            self.sessions[chat_id] = GroupSession(chat_id) # Initialize it
        
        self.sessions[chat_id].attach(member)

    def get_session(self, idCode) -> GroupSession:
        return self.sessions.get(idCode)
    
    def disconnect(self, chat_id: uuid.UUID, member: GroupMember) -> None:
        session = self.sessions.get(chat_id)
        session.disconnect(member)
        
        if len(session.members) == 0:
            self.sessions.pop(chat_id)
