from fastapi import FastAPI
from sqlmodel import SQLModel, select
from app.api.depends import SessionDep

from app.models.postgresDB.song import Song
from app.models.postgresDB.user import User
from app.models.postgresDB.guitar import Guitar
from app.models.postgresDB.g_string import GString
from app.models.postgresDB.category import Category
from app.models.postgresDB.level import Level  # 마지막에
app = FastAPI()

class WS(SQLModel):
    id: int
    name: str
    artist: str
    style: str
    speed: str
    level_id: int
    chord: str
    tube_url: str
    file_url: str
    categories: list[Category] = []

class DtoSong(SQLModel):
    name: str
    artist: str
    style: str
    speed: str
    level_id: int
    chord: str
    tube_url: str
    file_url: str
    category_ids: list[int] = []  # 카테고리 ID 리스트로 받음

class WowSong(DtoSong):
    id: int


class Ca(SQLModel):
    name: str
    ctype: str

class WowCa(Ca):
    id: int

class CaC(SQLModel):
    id: int
    name: str
    ctype: str
    songs: list[Song] = []

@app.get("/songs/{song_id}", response_model=WS)
async def get_songs(song_id: int, session: SessionDep):
    result = session.get(Song, song_id)
    return result

@app.get("/ca/{ca_id}", response_model=CaC)
async def get_ca(ca_id: int, session: SessionDep):
    result = session.get(Category, ca_id)
    return result

@app.get("/so")
async def get_so(session: SessionDep):
    result = session.exec(select(Song)).all()
    return result

@app.get("/cas")
async def get_so(session: SessionDep):
    result = session.exec(select(Category)).all()
    return result


@app.post("/songs")
def create_song(
        data: DtoSong,
        session: SessionDep
):
    # Song 생성 (category_ids 제외)
    song_data = data.model_dump(exclude={"category_ids"})
    song = Song(**song_data)

    # 카테고리 연결
    if data.category_ids:
        categories = session.exec(
            select(Category).where(Category.id.in_(data.category_ids))
        ).all()
        song.categories = categories

    session.add(song)
    session.commit()
    session.refresh(song)
    return song

@app.post("/categories")
async def create_category(session: SessionDep, ca: Ca):
    category = Category(**ca.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category