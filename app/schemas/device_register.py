from pydantic import BaseModel

class DeviceRegisterRequest(BaseModel):
    device_id: str