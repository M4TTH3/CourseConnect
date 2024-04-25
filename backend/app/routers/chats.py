from typing import Annotated
from fastapi import (
    APIRouter,
    Cookie,
    Depends,
    Query,
    WebSocket,
    WebSocketDisconnect
)
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

import logging

class GroupSession:
    """
        id_code: uniquely defines the group session
        members: holds connection for all connected members
    """

    id_code: int
    members: list[WebSocket]

    def __init__(self, idcode: int, ws: WebSocket) -> None:
        self.id_code = idcode
        self.members = [ws]

    def attach(self, ws: WebSocket) -> None:
        self.members.append(ws)

    def disconnect(self, ws: WebSocket) -> None:
        self.members.remove(WebSocket)

    async def sendAll(self, msg: str) -> None:
        "Sends the message to everyone in the group"
        for member in self.members:
            await member.send_text(msg)
    
    def __len__(self) -> int:
        return len(self.members)

class GroupSessionsManager:
    """
        Manages all the different group sessions happening at the same time
    """

    sessions: dict[int, GroupSession]

    def __init__(self) -> None:
        self.sessions = {}

    def attach(self, idcode: int, ws: WebSocket) -> None:
        session = self.sessions.get(idcode)

        if not session: 
            self.sessions[idcode] = GroupSession(idcode, ws)
        else:
            self.sessions[idcode].attach(ws)

        print(idcode)
        print(self.sessions[idcode].members)
        print(self.sessions)

    def getSession(self, idCode) -> GroupSession:
        return self.sessions.get(idCode)


manager = GroupSessionsManager()

router = APIRouter(prefix="/chats")

@router.get('/')
async def chat_home():
    return HTMLResponse("hello")


@router.websocket("/{idcode}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    idcode: int
):
    await websocket.accept()
    manager.attach(idcode, websocket)

    try:
        while True:
            data = await websocket.receive_text()

            await manager.getSession(idcode).sendAll(f"ID: {idcode}, Member Count: {len(manager.getSession(idcode))}, Sent: {data}")
    except WebSocketDisconnect:
        manager.getSession(idcode).disconnect(websocket)
        await manager.getSession(idcode).sendAll(f"User Disconnected; {len(manager.getSession(idcode))} members remaining.")
