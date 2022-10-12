from fastapi import WebSocket

class WSConnectionManager:
    def __init__(self):
        self.active_connections_map: dict = {}

    async def connect(self, user_pk: str, websocket: WebSocket):
        await websocket.accept()
        for pk, _ in self.active_connections_map.items():
            if pk == user_pk:
                print(">>Already connected")
                return
        self.active_connections_map[user_pk] = websocket

    def disconnect(self, user_pk: str):
        self.active_connections_map.pop(user_pk, None)

    async def send_json(self, sender_conn: WebSocket, to_pk, json: dict):
        for user_pk, connection in self.active_connections_map.items():
            if user_pk == to_pk:
                await connection.send_json(json)
        await sender_conn.send_json(json)

    async def broadcast_json(self, json: dict):
        for _, connection in self.active_connections_map.items():
            await connection.send_json(json)