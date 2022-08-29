from fastapi import APIRouter, Depends, Path, WebSocket, WebSocketDisconnect, Request
from lib.user_dependency import get_user_ws
from lib.ws_manager import WSConnectionManager
from services.message_service import MessageService

router = APIRouter()
manager = WSConnectionManager()
message_service = MessageService()

@router.websocket('/ws/chatroom/{chatroom_pk}')
async def ws_handler(
    websocket: WebSocket,
    chatroom_pk: str = Path(..., description="Chatroom primary key"),
    user: dict = Depends(get_user_ws)
):
    await manager.connect(websocket)
    try:
        while True:
            json: dict = await websocket.receive_json()
            if not json.get("message"):
                print("Error in client side")
                manager.disconnect(websocket)
            message, service_error = message_service.create_message(chatroom_pk, user["pk"], json.get("message"))
            if service_error:
                print(service_error)
                manager.disconnect(websocket)  
            await manager.broadcast_json({**message})
    except WebSocketDisconnect:
        manager.disconnect(websocket)