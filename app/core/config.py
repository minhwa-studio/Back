# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_url: str
    host: str
    port: int
    debug: bool
    jwt_secret: str  # ← 여기에 추가

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
