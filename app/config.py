from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb+srv://Ai-squad:4LcPfeuRrL5lPg2E@moiz.j9zaigt.mongodb.net/"
    DB_NAME: str = "isky_db"
    SECRET_KEY: str = "isky-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 ghante
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
