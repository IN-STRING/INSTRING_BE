from fastapi import FastAPI
from INewApp.core.config import settings
from fastapi.middleware.cors import CORSMiddleware


def instring_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )