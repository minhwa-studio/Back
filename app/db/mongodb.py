# app/db/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

from app.models.user import UserModel  # Beanie 모델

load_dotenv()  # .env 파일 로드

MONGO_URL = os.getenv("MONGO_URL")

async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client.get_default_database(), document_models=[UserModel])
