from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_url: str
    host: str
    port: int
    debug: bool

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
