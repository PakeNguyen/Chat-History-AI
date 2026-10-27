
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py nằm trong backend/app/core/
BACKEND_DIR = Path(__file__).resolve().parents[2]

# .env nằm tại thư mục gốc chat-history-ai/
ENV_FILE = BACKEND_DIR.parent / ".env"


class Settings(BaseSettings):
    app_name: str = "Chat History AI API"
    api_v1_prefix: str = "/api/v1"
    database_url: str
    log_level: str = "INFO"

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()
