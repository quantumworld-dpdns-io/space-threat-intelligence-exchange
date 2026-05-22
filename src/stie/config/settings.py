from __future__ import annotations

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "space-threat-intelligence-exchange"
    app_version: str = "0.1.0"
    app_debug: bool = False
    app_secret_key: str = "change-me-in-production"
    app_api_prefix: str = "/api/v1"
    app_cors_origins: list[str] = ["*"]

    database_url: str = "postgresql+asyncpg://stie:stie@localhost:5432/stie"
    database_pool_size: int = 20
    database_max_overflow: int = 10

    redis_url: str = "redis://localhost:6379/0"
    redis_password: str = ""

    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""
    qdrant_collection: str = "threat_reports"

    chroma_url: str = "http://localhost:8000"
    chroma_collection: str = "threat_reports"

    duckdb_path: str = "data/analytics.duckdb"

    iceberg_warehouse: str = "/data/iceberg"
    iceberg_catalog_uri: str = "http://localhost:8181"

    p2p_enabled: bool = True
    p2p_port: int = 9001
    p2p_bootstrap_peers: list[str] = []
    p2p_private_key: str = ""
    p2p_listen_addresses: list[str] = ["/ip4/0.0.0.0/tcp/9001"]

    ai_llm_provider: Literal["ollama", "openai", "vllm"] = "ollama"
    ai_llm_model: str = "gemma3"
    ai_llm_api_url: str = "http://localhost:11434"
    ai_llm_api_key: str = ""
    ai_embedding_model: str = "nomic-embed-text"
    ai_embedding_dimension: int = 768

    wandb_api_key: str = ""
    wandb_project: str = "stie-threat-intelligence"
    weave_enabled: bool = False

    auth_jwt_algorithm: str = "HS256"
    auth_jwt_expiration_minutes: int = 60
    auth_jwt_refresh_expiration_days: int = 7

    log_level: str = "INFO"
    log_format: Literal["json", "text"] = "json"

    metrics_enabled: bool = True
    opentelemetry_enabled: bool = False
    opentelemetry_endpoint: str = "http://localhost:4318"


settings = Settings()
