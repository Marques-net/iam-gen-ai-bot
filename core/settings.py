from __future__ import annotations

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "local"
    app_name: str = "iam-gen-ai-bot"
    log_level: str = "INFO"
    database_url: str
    redis_url: str
    llm_provider: str = "mock"
    search_provider: str = "mock"
    whatsapp_provider: str = "mock"
    whatsapp_verify_token: str | None = None
    whatsapp_app_secret: str | None = None
    whatsapp_access_token: str | None = None
    whatsapp_phone_number_id: str | None = None
    whatsapp_from_number: str | None = None
    workspace_default_language: str = "pt-BR"
    timezone: str = "America/Sao_Paulo"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
