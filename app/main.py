from fastapi import FastAPI
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()



app.include_router(api_router, prefix="/api/v1")