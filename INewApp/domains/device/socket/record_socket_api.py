import os
import json
import uuid
from sqlmodel import select
from fastapi import APIRouter, WebSocket
from INewApp.core.dependencies import AsyncSessionLocal
from INewApp.domains.users.models.user_table import User
from INewApp.domains.record.models.record_table import UserRecord
from INewApp.domains.ai.SAT_model.SAT_predict import FSpredictor
from INewApp.domains.ai.chord_model.chord_predict import Cpredictor
from INewApp.domains.device.service.connect_socket import manager
from INewApp.domains.device.service.s3_upload_data import upload_s3
from INewApp.domains.device.service.audio_img import create_audio_img


device_socket_router = APIRouter()


TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)


@device_socket_router.websocket("/ws/device/{device_id}")
async def ws_sensor_device(websocket: WebSocket, device_id: str):
    await manager.connect_device(device_id, websocket)

    file = None
    file_path = None
    file_name = None

    try:
        while True:
            message = await websocket.receive()
            print("메시지", message)

            if message["type"] == "websocket.disconnect":
                break

            if "text" in message:
                print("텍스트 json", message)
                data = json.loads(message["text"])

                if data["type"] == "file_start":
                    print("녹음 시작", message)

                    raw_name = data["name"]
                    file_name = os.path.basename(raw_name)

                    unique_id = uuid.uuid4().hex[:8]
                    file_path = os.path.join(TEMP_DIR, f"{device_id}_{unique_id}_{file_name}")
                    file = open(file_path, "wb")

                elif data["type"] == "file_end":
                    print("녹음 끝남", message)
                    if file:
                        file.close()
                        file = None

                        async with AsyncSessionLocal() as session:
                            result = await session.exec(
                                select(User).where(User.device_id == device_id)
                            )
                            user = result.first()

                        if not user:
                            await websocket.send_text(json.dumps({
                                "type": "error",
                                "message": "등록되지 않은 기기입니다"
                            }))
                            os.remove(file_path)
                            continue

                        file_url = upload_s3.upload_record_song(file_path, f"{device_id}_{unique_id}_{file_name}")
                        img_path = file_path.replace(".wav", ".png")
                        create_audio_img(file_path, img_path)
                        spec_img_url = upload_s3.upload_record_image(img_path, f"{device_id}_{unique_id}_{file_name.replace('.wav', '.png')}")

                        async with AsyncSessionLocal() as session:
                            result = await session.exec(
                                select(User).where(User.device_id == device_id)
                            )
                            user = result.first()

                        song_chord = Cpredictor.predict_result(file_url)
                        song_style_speed = FSpredictor.analyze_guitar_performance(file_url)

                        async with AsyncSessionLocal() as session:
                            if user:
                                record = UserRecord(
                                    name=file_name,
                                    style=song_style_speed["style"],
                                    chord=song_chord,
                                    speed=song_style_speed["tempo"],
                                    file_url=file_url,
                                    spec_img_url=spec_img_url,
                                    user_id=user.id,
                                )
                                session.add(record)
                                await session.commit()

                        await manager.send_to_front(device_id, json.dumps({
                            "type": "record_complete"
                        }))

                        os.remove(file_path)
                        os.remove(img_path)

                else:
                    print("온습도",message)
                    await manager.send_to_front(device_id, message["text"])

            elif "bytes" in message:
                print("녹음 바이트", message)
                if file:
                    file.write(message["bytes"])

    except Exception as e:
        print(f"{device_id} 에러: {e}")

    finally:
        manager.disconnect_device(device_id)
        if file:
            file.close()