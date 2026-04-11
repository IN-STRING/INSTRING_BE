from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from INewApp.core.dependencies import SessionDep
from INewApp.domains.users.models.user_table import User
from INewApp.core.security.jwt_token import jwt_manager
from INewApp.domains.device.service.connect_socket import manager


front_socket_router = APIRouter()


@front_socket_router.websocket("/ws/front")
async def socket_front(session: SessionDep, websocket: WebSocket):

    userdata = await jwt_manager.check_token_ws(websocket)
    user = await session.get(User, int(userdata["sub"]))
    await manager.connect_front(user.device_id, websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect_front(user.device_id)