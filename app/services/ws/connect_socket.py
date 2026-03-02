from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.front_connections: Dict[str, WebSocket] = {}

    async def connect_front(self, device_id: str, websocket: WebSocket):
        await websocket.accept()
        self.front_connections[device_id] = websocket

    def disconnect_front(self, device_id: str):
        self.front_connections.pop(device_id, None)

    async def send_to_front(self, device_id: str, message: str):
        websocket = self.front_connections.get(device_id)
        if websocket:
            await websocket.send_text(message)

manager = ConnectionManager()