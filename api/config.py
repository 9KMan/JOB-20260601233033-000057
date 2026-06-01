from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "MongoDB to Postgres Migration API"
    debug: bool = False
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "source_db"
    postgres_uri: str = "postgresql://user:pass@localhost:5432/target_db"
    jwt_secret: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()