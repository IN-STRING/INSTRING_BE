from pydantic import BaseModel
from app.models.postgresDB.category import Category

class SongS(BaseModel):
    id: int
    name: str
    artist: str
    level_id: int

class WS(BaseModel):
    id: int
    name: str
    artist: str
    style: str
    speed: str
    level_id: int
    chord: str
    tube_url: str
    # file_url: str
    categories: list[Category] = []