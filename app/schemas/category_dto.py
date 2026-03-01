from pydantic import BaseModel
from app.schemas.song_dto import SongS

class SearchCategory(BaseModel):
    songs: list[SongS] = []