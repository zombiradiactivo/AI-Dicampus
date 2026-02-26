import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    PROJECT_NAME: str = "CollabTaskManager"
    API_VERSION: str = "v1"
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev_secret_key_99x")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    RATE_LIMIT_PER_MINUTE: int = 100
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///app.db")

settings = Config()