from pydantic import BaseModel

class ModalDTO(BaseModel):
    modal: bool
    device: bool
    strings: str
    levels: str