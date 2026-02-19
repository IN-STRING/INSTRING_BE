from app.core.db_engine import engine
from sqlmodel import Session
from typing import Annotated
from fastapi import Depends
from jwt.exceptions import InvalidTokenError

def get_session():
    with Session(bind=engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]