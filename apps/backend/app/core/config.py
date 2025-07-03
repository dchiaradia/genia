from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

print(f"env path: {ENV_PATH}")

class Settings(BaseSettings):
    APP_NAME: str = "My FastAPI Service"
    API_V1_STR: str = "/api/v1"
    API_DOCS_URL: str = f"{API_V1_STR}/docs"
    DEBUG: bool = True

    # variáveis obrigatórias do banco
    EMBEDDING_DIM: int = 1536
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    
    # KAFKA SETTINGS
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC_PREFIX: str
    
    # AZURE - Chat completion
    AZURE_OPEN_AI_CHAT_COMPLETION_URI: str
    AZURE_OPEN_AI_CHAT_COMPLETION_KEY: str
    AZURE_OPEN_AI_CHAT_COMPLETION_VERSION: str
    AZURE_OPEN_AI_CHAT_COMPLETION_NAME: str
    AZURE_OPEN_AI_CHAT_COMPLETION_MODEL_NAME: str
    
    
    # AZURE LLM - Embedding
    AZURE_OPEN_AI_EMBEDDING_URI: str
    AZURE_OPEN_AI_EMBEDDING_KEY: str
    AZURE_OPEN_AI_EMBEDDING_VERSION: str
    AZURE_OPEN_AI_EMBEDDING_NAME: str
    AZURE_OPEN_AI_EMBEDDING_MODEL_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
    )

# instância global
settings = Settings()
