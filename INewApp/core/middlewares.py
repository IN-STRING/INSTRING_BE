from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def instring_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 나중에 프론트 url 추가
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )