from fastapi import APIRouter, Depends, Path, WebSocket, WebSocketDisconnect, Request
from lib.user_dependency import get_user_ws
from lib.ws_manager import WSConnectionManager
from services.message_service import MessageService
import config

router = APIRouter()
manager = WSConnectionManager()
message_service = MessageService()

@router.websocket('/ws/chatroom/{chatroom_pk}')
async def ws_handler(
    websocket: WebSocket,
    chatroom_pk: str = Path(..., description="Chatroom primary key"),
    user: dict = Depends(get_user_ws)
):
    await manager.connect(user["pk"], websocket)
    await manager.broadcast_json({"type": "connection", "user_pk": user["pk"]})
    try:
        while True:
            json: dict = await websocket.receive_json()
            if not json.get("message") and not json.get("to_pk"):
                if config.debugging: print(">>>> WS ERROR: Error in client side")
                raise WebSocketDisconnect()
            message, service_error = message_service.create_message(chatroom_pk, user["pk"], json.get("message"))
            if service_error:
                if config.debugging: print(">>>> WS SERVICE ERROR:", service_error)
                raise WebSocketDisconnect()
            await manager.send_json(websocket, json.get("to_pk"), {"type": "message", **message})
    except WebSocketDisconnect:   
        manager.disconnect(user["pk"])