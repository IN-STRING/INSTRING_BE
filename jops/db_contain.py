from sqlmodel import Session
from app.core.db_engine import engine
from app.models.postgresDB.guitar import Guitar
from app.models.postgresDB.level import Level
from app.models.postgresDB.g_string import GString
from app.schemas.gstring_val import GStringEnum
from app.schemas.guitar_val import GuitarVal
from app.schemas.level_step import LevelStep

with Session(engine) as session:
    strings = [GString(name="s1", step=GStringEnum.normal), GString(name="s2", step=GStringEnum.coting)]
    levels = [Level(name="l1", step=LevelStep.L1),Level(name="l2", step=LevelStep.L2),Level(name="l3", step=LevelStep.L3),Level(name="l4", step=LevelStep.L4),Level(name="l5", step=LevelStep.L5)]
    guitars = [Guitar(name="g1", step=GuitarVal.g1),Guitar(name="g2", step=GuitarVal.g2),Guitar(name="g3", step=GuitarVal.g3),Guitar(name="g4", step=GuitarVal.g4)]

    for s in strings:
        session.add(s)
    for l in levels:
        session.add(l)
    for g in guitars:
        session.add(g)

    session.commit()