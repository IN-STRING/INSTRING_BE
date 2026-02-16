from pydantic import BaseModel

class ModalDTO(BaseModel):
    modal: bool
    machinery: bool
    strings: str
    levels: str
    guitars: str