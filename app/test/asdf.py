# from sqlalchemy.orm import configure_mappers
# from app.models.postgresDB.base import Base
#
# import app.models.postgresDB.song as song_mod
# import app.models.postgresDB.level as level_mod
#
# Song = song_mod.Song
# Level = level_mod.Level
#
# print("Song module:", Song.__module__)
# print("Level module:", Level.__module__)
#
# print("Song in registry?:", "Song" in Base.registry._class_registry)
# print("Registry['Song']:", Base.registry._class_registry.get("Song"))
#
# print("metadata ids:", id(Song.metadata), id(Level.metadata), id(Base.metadata))
# print("same metadata?:", Song.metadata is Level.metadata is Base.metadata)
#
# # 레지스트리 키 중 Song 비슷한 거 있는지
# keys = [k for k in Base.registry._class_registry.keys() if isinstance(k, str) and "Song" in k]
# print("registry keys containing 'Song':", keys)
#
# try:
#     configure_mappers()
#     print("configure_mappers OK")
# except Exception as e:
#     print("configure_mappers ERROR:", repr(e))
#     raise

# from sqlmodel import SQLModel
# from sqlalchemy.orm import configure_mappers
#
# from app.models.postgresDB.song import Song
# from app.models.postgresDB.level import Level
#
# reg = SQLModel.__sqlalchemy_registry__._class_registry
#
# print("Song in registry?:", "Song" in reg)
# print("Level in registry?:", "Level" in reg)
# print("reg['Song']:", reg.get("Song"))
#
# try:
#     configure_mappers()
#     print("configure_mappers OK")
# except Exception as e:
#     print("configure_mappers ERROR:", repr(e))
#     raise

import sqlmodel, sqlalchemy, pydantic
from sqlmodel import SQLModel
from app.models.postgresDB.song import Song
from app.models.postgresDB.level import Level

print("versions:", sqlmodel.__version__, sqlalchemy.__version__, pydantic.__version__)

sa_reg = getattr(SQLModel, "_sa_registry", None)
print("SQLModel._sa_registry:", sa_reg)

print("metadata tables:", list(SQLModel.metadata.tables.keys()))

if sa_reg is not None:
    reg = sa_reg._class_registry
    print("Song in registry?:", "Song" in reg)
    print("Level in registry?:", "Level" in reg)
    print("keys containing 'Song':", [k for k in reg.keys() if "Song" in str(k)])

print("Song mapped?:", hasattr(Song, "__table__"), getattr(Song, "__tablename__", None))
print("Level mapped?:", hasattr(Level, "__table__"), getattr(Level, "__tablename__", None))