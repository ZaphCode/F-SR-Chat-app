from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from lib.ws_manager import WSConnectionManager

router = APIRouter()
manager = WSConnectionManager()

@router.websocket('/ws')
async def ws_handler(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            json = await websocket.receive_json()
            print(json)
            await manager.broadcast_json(json)
    except WebSocketDisconnect:
        manager.disconnect(websocket)