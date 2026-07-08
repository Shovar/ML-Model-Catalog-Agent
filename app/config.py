import os


class Settings:
    llm_endpoint: str = os.getenv("LLM_ENDPOINT", "http://localhost:11434/v1")
    llm_model: str = os.getenv("LLM_MODEL", "qwen2.5:3b")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///catalogue.db")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "not-needed")


settings = Settings()
