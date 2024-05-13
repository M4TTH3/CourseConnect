from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Security, HTTPException
from ..internal.chats_util import GroupSessionsManager, GroupSession, GroupMember
import uuid
from ..internal.auth import AuthUser, auth
from ..internal import crud, schemas
from sqlalchemy.orm import Session
from pydantic import ValidationError

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
    Second check the chat exists and the user is a part of the chat 
    """
    try:
        auth_header = websocket.headers.get('Authorization')
        auth_user: AuthUser = await verify_from_header(ws=websocket, auth_header=auth_header)
        chat = crud.get_chat(db, chat_id)
        
        if not chat or not auth_user: raise Exception()
        
        # Check the user is in the chat
        if not auth_user.uid in [user.id for user in chat.users]: raise Exception()
    except Exception as e:
        # Error close the socket and return
        await websocket.close()
        return
    
    """
    Send and update responses
    """
    await websocket.accept()
    
    user = GroupMember(ws=websocket, id=auth_user.uid)
    manager.attach(chat_id, user)
    
    session = manager.get_session(chat_id)
    
    # First send the first scroll message
    await session.scroll(user, db)
    

    while True:
        try:
            data = await user.get_ws().receive_json()
            data_formatted = schemas.ChatAction.model_validate(data)
            
            match data_formatted.action.lower():
                case 'send':
                    await session.send(data_formatted.payload, auth_user.uid, db)
                case 'delete':
                    await session.delete_message(data_formatted.payload, auth_user.uid, db)
                case 'scroll':
                    await session.scroll(user, db)

        except WebSocketDisconnect:
            manager.disconnect(chat_id, user)
            return

        except ValidationError as e:
            await user.get_ws().send_text(schemas.ChatResponse(action='error', payload="Bad payload format").model_dump_json())

        except Exception as e:
            await user.get_ws().send_text(schemas.ChatResponse(action='error', payload=str(e)).model_dump_json())
