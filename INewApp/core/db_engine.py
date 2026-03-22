from sqlmodel import create_engine
from INewApp.core.config import settings


SQLALCHEMY_DATABASE_URI = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)