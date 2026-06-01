from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_router
from api.config import settings
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "MongoDB to PostgreSQL Migration API", "version": "1.0.0"}