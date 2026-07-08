from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.database import get_session
from catalogue.schema import MetricSnapshot, Model


def get_model_status(model_id: str) -> dict:
    session: Session
    with get_session() as session:
        model = session.get(Model, model_id)
        if model is None:
            return {"error": f"Model with id '{model_id}' not found."}

        return {
            "id": model.id,
            "name": model.name,
            "version": model.version,
            "framework": model.framework,
            "task_type": model.task_type,
            "environment": model.environment,
            "owner_team": model.owner_team,
            "status": model.status,
            "last_deployed_at": model.last_deployed_at,
            "cost_per_month_usd": model.cost_per_month_usd,
            "kpi_supported": model.kpi_supported,
            "notes": model.notes,
        }


def list_stale_models(threshold_days: int = 30) -> list[dict]:
    session: Session
    cutoff = (datetime.now(timezone.utc) - timedelta(days=threshold_days)).isoformat()
    with get_session() as session:
        rows = (
            session.query(Model)
            .filter(Model.last_deployed_at < cutoff)
            .all()
        )
        return [
            {
                "id": m.id,
                "name": m.name,
                "environment": m.environment,
                "status": m.status,
                "last_deployed_at": m.last_deployed_at,
            }
            for m in rows
        ]


def get_latency_metrics(model_id: str, hours: int = 24) -> dict:
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    session: Session
    with get_session() as session:
        model = session.get(Model, model_id)
        if model is None:
            return {"error": f"Model with id '{model_id}' not found."}

        snapshots = (
            session.query(MetricSnapshot)
            .filter(
                MetricSnapshot.model_id == model_id,
                MetricSnapshot.captured_at >= cutoff,
            )
            .order_by(MetricSnapshot.captured_at.desc())
            .all()
        )

        return {
            "model_id": model_id,
            "model_name": model.name,
            "lookback_hours": hours,
            "snapshots": [
                {
                    "captured_at": s.captured_at,
                    "latency_p95_ms": s.latency_p95_ms,
                    "drift_score": s.drift_score,
                    "accuracy_score": s.accuracy_score,
                    "availability_pct": s.availability_pct,
                }
                for s in snapshots
            ],
        }
