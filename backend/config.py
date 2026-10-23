"""Central configuration loaded from environment / .env (never hard-code secrets)."""
from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    gemini_api_key: SecretStr = SecretStr("")
    gemini_model: str = "gemini-2.5-flash"
    database_url: str = f"sqlite:///{BASE_DIR / 'data' / 'job_agent.db'}"
    mock_mode: bool = True
    max_upload_mb: int = 5
    log_level: str = "INFO"

    @property
    def gemini_configured(self) -> bool:
        return bool(self.gemini_api_key.get_secret_value().strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()
