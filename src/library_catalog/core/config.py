from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Добавить все поля
    app_name: str
    environment: Literal["development", "staging", "production"]
    debug: bool
    database_url: PostgresDsn
    database_pool_size: int
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()