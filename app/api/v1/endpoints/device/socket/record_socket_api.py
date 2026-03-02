import os
import json
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.ws.connect_socket import manager
from app.core.s3.connect_s3 import upload_to_s3
from app.services.audio.audio_img import create_audio_img

record_socket_router = APIRouter()

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

@record_socket_router.websocket("/ws/record/device/{device_id}")
async def ws_sensor_device(websocket: WebSocket, device_id: str):
    await websocket.accept()

    file = None
    file_path = None
    file_name = None

    try:
        while True:
            message = await websocket.receive()

            if "text" in message:
                data = json.loads(message["text"])

                if data["type"] == "file_start":
                    file_name = data["name"]
                    unique_id = uuid.uuid4().hex[:8]
                    file_path = os.path.join(TEMP_DIR, f"{device_id}_{unique_id}_{file_name}")
                    file = open(file_path, "wb")

                elif data["type"] == "file_end":
                    if file:
                        file.close()
                        file = None

                        s3_key = f"records/{device_id}/{unique_id}_{file_name}"
                        file_url = upload_to_s3(file_path, s3_key, "audio/wav")

                        img_path = file_path.replace(".wav", ".png")
                        create_audio_img(file_path, img_path)
                        img_s3_key = s3_key.replace(".wav", ".png")
                        spec_img_url = upload_to_s3(img_path, img_s3_key, "image/png")

                        await manager.send_to_front(device_id, json.dumps({
                            "type": "record_complete",
                            "file_url": file_url,
                            "spec_img_url": spec_img_url,
                        }))

                        os.remove(file_path)
                        os.remove(img_path)

            elif "bytes" in message:
                if file:
                    file.write(message["bytes"])

    except WebSocketDisconnect:
        if file:
            file.close()