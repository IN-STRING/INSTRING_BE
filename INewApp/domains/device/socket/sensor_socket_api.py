from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from INewApp.domains.device.service.connect_socket import manager


sensor_socket = APIRouter()


@sensor_socket.websocket("/ws/sensor/device/{device_id}")
async def socket_websocket(websocket: WebSocket, device_id: str):

    await manager.connect_device(device_id, websocket)

    try:
        while True:
            raw = await websocket.receive_text()
            await manager.send_to_front(device_id, raw)

    except WebSocketDisconnect:
        manager.disconnect_device(device_id)