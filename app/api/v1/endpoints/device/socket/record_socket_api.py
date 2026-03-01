from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.api.depends import SessionDep
from app.services.ws.record_socket.record_file_socket import record_manager

record_socket_api = APIRouter()

