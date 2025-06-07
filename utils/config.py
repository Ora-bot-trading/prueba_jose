from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./trading_bot.db"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Trading Parameters
    MAX_TRADE_SIZE: float = 1000.0
    STOP_LOSS_PERCENTAGE: float = 2.0
    TAKE_PROFIT_PERCENTAGE: float = 5.0
    
    # API Keys
    BINANCE_API_KEY: str = ""
    BINANCE_API_SECRET: str = ""
    TELEGRAM_BOT_TOKEN: str = ""
    
    # Monitoring
    SENTRY_DSN: str = ""
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
