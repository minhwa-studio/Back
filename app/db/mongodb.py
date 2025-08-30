# app/db/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

from app.models.user import UserModel

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = "mydb"  # <-- 여기에 명시적으로 DB 이름 설정

async def init_db():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]  # <-- get_default_database() 대신 직접 접근
    await init_beanie(database=db, document_models=[UserModel])
