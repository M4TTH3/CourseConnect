from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from ..internal.chats_util import GroupSessionsManager, GroupSession, Message

manager = GroupSessionsManager()

router = APIRouter(prefix="/chats")

@router.websocket("/{idcode}/ws")
async def websocket_endpoint(*, websocket: WebSocket, idcode: int):
    await websocket.accept()
    manager.attach(idcode, websocket)
    session = manager.getSession(idcode)

    try:
        while True:
            data = await websocket.receive_text()

            await session.sendAll(
                f"ID: {idcode}, Member Count: {len(manager.getSession(idcode))}, Sent: {data}"
            )
    except WebSocketDisconnect:
        session.disconnect(websocket)
        await session.sendAll(
            f"User Disconnected; {len(manager.getSession(idcode))} members remaining."
        )
