from sqlmodel import Field, Relationship
from typing import Optional
from app.models.postgresDB.base import Base
from app.models.postgresDB.level import Level

class Song(Base, table=True):
    name: str
    artist: str
    style: str
    speed: str
    level_id: Optional[int] = Field(default=None, foreign_key="level.id", index=True)
    # category_id: Optional[int] = Field(default=None, foreign_key="category.id", index=True)
    chord: str
    tube_url: str
    file_url: str

    song_level: Level = Relationship(back_populates="songs")


# DDD
# 헥사고날
# MSA
# 클린 아케텍처
#
# - 특징? 장르 (bpm 그런거임) (박하원) O 일대다
# - 작곡가 등 O 일대다
# - 곡의 코드 (이시우) O
# - 분류 (스트로크, 아르페지오, 핑거) (박하원) O 다대다
# - 제목 O
# - 곡의 유튜브 url O
# - 저장소 url
# - 난이도 O 일대다