from pydantic import BaseModel
from INewApp.common.common_models.category import Category

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


class SearchCategory(BaseModel):
    songs: list[SongS] = []