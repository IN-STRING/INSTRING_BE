from sqlmodel import Field
from typing import Optional
from app.models.postgresDB.base import Base

class Song(Base, table=True):
    pass

# DDD
# 헥사고날
# MSA
# 클린 아케텍처