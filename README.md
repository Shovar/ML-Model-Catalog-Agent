# ML Model Catalogue Agent

A LangChain-powered AI agent that answers questions about an ML model catalogue using tool calls. Runs locally with FastAPI + SQLite + vLLM.

## Architecture

```
POST /chat  →  LangChain Agent  →  Tools  →  SQLite Catalogue
                        ↕
                   vLLM (local)
```

The agent has **3 tools** — it *must* call them for factual answers (no hallucination):

| Tool | What it does |
|---|---|
| `get_model_status(model_id)` | Status, owner, environment, deployment metadata |
| `list_stale_models(threshold_days)` | Models not updated/deployed past N days |
| `get_latency_metrics(model_id, hours)` | Recent p95 latency, drift, accuracy, availability |

## Quick start

```bash
# 1. Install
pip install -e ".[dev]"

# 2. Seed the database
make seed

# 3. Start the API
make run

# 4. In another terminal, ask it questions
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Which models are stale?"}'
```

## Example questions

- `"Which models are stale?"`
- `"What is the latency of model mod-001?"`
- `"Show me the details of model fraud-detection-v2"` (note: it needs the model ID)
- `"Which models are in production?"`
- `"Do we have any decommissioned models?"`

## API response format

```json
{
  "answer": "The following 4 models are stale (not deployed for over 30 days)...",
  "tool_calls_used": [
    {
      "tool_name": "list_stale_models",
      "arguments": {"threshold_days": 30},
      "raw_output": "[{\"id\": \"mod-003\", ...}]"
    }
  ],
  "evidence": [
    {
      "tool_name": "list_stale_models",
      "arguments": {},
      "raw_output": "[{\"id\": \"mod-003\", ...}]"
    }
  ]
}
```

## Database (catalogue.db)

7 seeded models across `production`, `staging`, `development`:

| ID | Name | Status | Team |
|---|---|---|---|
| mod-001 | fraud-detection-v2 | active | risk-analytics |
| mod-002 | recommendation-engine | active | personalization |
| mod-003 | sentiment-classifier | active | nlp |
| mod-004 | churn-predictor | decommissioned | growth |
| mod-005 | image-classifier | inactive | cv |
| mod-006 | anomaly-detection-stream | active | ml-platform |
| mod-007 | pricing-optimizer | active | pricing |

Plus 8 metric snapshots with latency, drift, accuracy, and availability readings.

## Configuration (env vars)

| Variable | Default | Description |
|---|---|---|
| `VLLM_ENDPOINT` | `http://localhost:8001/v1` | vLLM OpenAI-compatible endpoint |
| `VLLM_MODEL` | `Qwen/Qwen2.5-3B-Instruct` | Model name served by vLLM |
| `DATABASE_URL` | `sqlite:///catalogue.db` | SQLite database path |

## Docker

```bash
docker-compose up --build
```

Then `curl` the same `/chat` endpoint on port 8000.

## Kubernetes

```bash
kubectl apply -f k8s/deployment.yaml
```

The deployment expects a `vllm-service` to be running in the cluster for the agent to call.

## Commands

| Command | What it does |
|---|---|
| `make seed` | Seed SQLite with models and metrics |
| `make run` | Start dev server on `:8000` |
| `make lint` | Run ruff |
| `make clean` | Delete database and caches |
