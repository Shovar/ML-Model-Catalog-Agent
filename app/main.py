from fastapi import FastAPI

from app.api import router

app = FastAPI(
    title="ML Model Catalogue Agent",
    description="A LangChain agent that queries a simulated ML model catalogue using local LLM inference.",
    version="0.1.0",
)

app.include_router(router)
