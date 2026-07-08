import os


class Settings:
    vllm_endpoint: str = os.getenv("VLLM_ENDPOINT", "http://localhost:8001/v1")
    vllm_model: str = os.getenv("VLLM_MODEL", "Qwen/Qwen2.5-3B-Instruct")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///catalogue.db")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "not-needed")


settings = Settings()
