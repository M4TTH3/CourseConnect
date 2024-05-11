from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Security, HTTPException
from ..internal.chats_util import GroupSessionsManager, GroupSession, Message
import uuid
from ..internal.auth import AuthUser, auth
from ..internal import crud, schemas, db_models as models
from sqlalchemy.orm import Session

from typing import Optional

manager = GroupSessionsManager()

router = APIRouter(prefix="/chats")

@router.delete("/leave/{chat_id}", response_model=schemas.User)
def leave_chat(chat_id: uuid.UUID, auth_result: AuthUser = Security(auth.verify, scopes=['readwrite:post']), db: Session = Depends(crud.get_db)):
    return crud.leave_chat(db, chat_id=chat_id, user_id=auth_result.uid)


async def verify_from_header(ws: WebSocket, auth_header: str) -> AuthUser:
    if not auth_header: raise "No auth header"
    
    bearer, token = auth_header.split(' ')
    if not bearer or bearer.lower() != 'bearer' or not token: raise "Bad header format"
    
    auth_user: AuthUser = await auth.verify_std(['read:groupchat', 'write:groupchat'], token)
    return auth_user

@router.websocket("/{chat_id}/ws")
# https://github.com/tiangolo/fastapi/issues/2031
async def websocket_endpoint(
    websocket: WebSocket, 
    chat_id: uuid.UUID, 
    db: Session = Depends(crud.get_db)
):
    """
    First extract the bearer token and verify the token
    Second check the chat exists and the user is inside the chat 
    """
    try:
        auth_header = websocket.headers.get('Authorization')
        auth_user: AuthUser = await verify_from_header(ws=websocket, auth_header=auth_header)
        chat = crud.get_chat(db, chat_id)
        
        if not chat or not auth_user: raise Exception()
        
        # Check the user is in the chat
        if not auth_user.uid in [user.id for user in chat.users]: raise Exception()
    except:
        await websocket.close()
        return
    
    """
    Send and update responses
    """
    await websocket.accept()
    # await websocket.send_text(str(bearer_token))
    manager.attach(chat_id, websocket)
    session = manager.getSession(chat_id)
    
    try:
        while True:
            data = await websocket.receive_json()

            await session.sendAll(
                f"ID: {chat_id}, Member Count: {len(manager.getSession(chat_id))}, Sent: {data}"
            )
    except WebSocketDisconnect:
        session.disconnect(websocket)
        await session.sendAll(
            f"User Disconnected; {len(manager.getSession(chat_id))} members remaining."
        )
