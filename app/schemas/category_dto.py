from pydantic import BaseModel
from app.models.postgresDB.song import Song

class SearchCategory(BaseModel):
    id: int
    name: str
    ctype: str
    songs: list[Song] = []