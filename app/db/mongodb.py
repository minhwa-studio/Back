from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os

from app.models.user import User  # Beanie 모델

MONGO_URL = os.getenv("MONGO_URL")

async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    await init_beanie(database=client["mydb"], document_models=[User])
