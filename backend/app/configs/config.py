from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    JWT_KEY: str
    ALGORITHM: str
    JWT_TOKEN_EXPIRE: int
    CORS_ORIGINS: str
    MAX_IMAGE_SIZE_MB: int
    GEMINI_API_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        import urllib.parse
        user = urllib.parse.quote_plus(self.DB_USER)
        password = urllib.parse.quote_plus(self.DB_PASSWORD)
        return f"postgresql://{user}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
