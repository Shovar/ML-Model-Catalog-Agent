from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from app.config import settings
from app.tools import get_latency_metrics as _get_latency_metrics
from app.tools import get_model_status as _get_model_status
from app.tools import list_stale_models as _list_stale_models


@tool
def get_model_status(model_id: str) -> dict:
    """Retrieve the status, owner team, environment, and deployment metadata for a model by its ID."""
    return _get_model_status(model_id)


@tool
def list_stale_models(threshold_days: int = 30) -> list[dict]:
    """Return models whose last update or deployment is older than the given threshold in days."""
    return _list_stale_models(threshold_days)


@tool
def get_latency_metrics(model_id: str, hours: int = 24) -> dict:
    """Retrieve recent latency measurements and metrics for a model by its ID."""
    return _get_latency_metrics(model_id, hours)


tools = [get_model_status, list_stale_models, get_latency_metrics]

SYSTEM_PROMPT = (
    "You are an ML model catalogue assistant. "
    "You have access to tools that query a database of ML models and their metrics. "
    "Always use the tools to answer factual questions. "
    "Do not fabricate metadata or metrics. "
    "Base your answers strictly on the tool output. "
    "If you need a model ID but only have a name, ask the user for the model ID. "
    "Be concise and direct in your answers."
)

llm = ChatOpenAI(
    model=settings.llm_model,
    base_url=settings.llm_endpoint,
    api_key=settings.openai_api_key,
    temperature=0,
)

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
)
