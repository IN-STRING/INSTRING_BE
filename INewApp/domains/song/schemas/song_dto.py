from fastapi import Form
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
    categories: list[Category] = []


class SearchCategory(BaseModel):
    songs: list[SongS] = []


class SongCreateRequest(BaseModel):
    name: str
    artist: str
    level_id: int
    tube_url: str

    chord: str = ""
    speed: str = ""
    style: str = ""
    file_url: str = ""

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        artist: str = Form(...),
        level_id: int = Form(...),
        youtube_url: str = Form(...),
    ):
        return cls(
            name=name,
            artist=artist,
            level_id=level_id,
            tube_url=youtube_url
        )