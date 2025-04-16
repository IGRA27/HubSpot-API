from pydantic import BaseSettings, Field
from functools import lru_cache

class Settings(BaseSettings):
    # --- Cloudant ---
    cloudant_url: str = Field(..., env="CLOUDANT_URL")
    cloudant_api_key: str = Field(..., env="CLOUDANT_APIKEY")
    db_name: str = "mydb"

    # --- Elasticsearch ---
    elastic_hosts: str = Field(..., env="ELASTIC_HOSTS")          # coma‑separados
    rag_index: str = "rag-index"

    # --- HubSpot ---
    hubspot_token: str = Field(..., env="HUBSPOT_TOKEN")

    # --- App ---
    app_name: str = "RAG‑HubSpot API"
    app_version: str = "0.1.0"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Settings cached para inyección."""
    return Settings()
