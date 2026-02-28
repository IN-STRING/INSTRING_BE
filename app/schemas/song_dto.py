from pydantic import BaseModel
from app.models.postgresDB.category import Category

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