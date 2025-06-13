from pydantic import BaseSettings
import os
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")  

if not DATABASE_URL or not SECRET_KEY or not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise ValueError("Missing environment variables")

class Settings(BaseSettings):
    DATABASE_URL: str = DATABASE_URL
    SECRET_KEY: str = SECRET_KEY
    ALGORITHM: str = ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(ACCESS_TOKEN_EXPIRE_MINUTES) 

    class Config:
        env_file = ".env"

settings = Settings()
