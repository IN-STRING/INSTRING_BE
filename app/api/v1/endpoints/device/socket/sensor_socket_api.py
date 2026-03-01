from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.api.depends import SessionDep
from app.models.postgresDB.user import User
from app.core.security.jwt_token import jwt_manager
from app.services.ws.sensor_socket.temperature_humidity_socket import manager

socket_router = APIRouter()

@socket_router.websocket("/ws/front")
async def socket_front(session: SessionDep, websocket: WebSocket):

    userdata = await jwt_manager.check_token_ws(websocket)
    user = session.get(User, userdata["sub"])
    await manager.connect_front(user.device_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect_front(user.device_id)


@socket_router.websocket("/ws/sensor/device/{device_id}")
async def socket_websocket(websocket: WebSocket, device_id: str):

    await websocket.accept()

    try:
        while True:
            raw = await websocket.receive_text()
            await manager.send_to_front(device_id, raw)

    except WebSocketDisconnect:
        pass