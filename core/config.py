from functools import lru_cache  
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):  
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    jwt_secret: str  
    jwt_algorithm: str = "HS256"  
    access_token_ttl_minutes: int = 30  
    database_url: str = "sqlite:///./video_games_data.db"


@lru_cache  
def get_settings() -> Settings:  
    return Settings(jwt_secret=os.getenv("JWT_SECRET") or "")  