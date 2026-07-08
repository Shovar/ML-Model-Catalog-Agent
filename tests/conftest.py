from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from catalogue.schema import Base, MetricSnapshot, Model


@pytest.fixture
def db_session(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    def mock_get_session():
        return Session(engine)

    monkeypatch.setattr("app.database.get_session", mock_get_session)
    monkeypatch.setattr("app.tools.get_session", mock_get_session)

    now = datetime.now(timezone.utc)

    with Session(engine) as session:
        models = [
            Model(
                id="mod-001",
                name="test-model-a",
                framework="scikit-learn",
                version="1.0",
                task_type="classification",
                environment="production",
                owner_team="team-a",
                status="active",
                last_deployed_at=(now - timedelta(days=5)).isoformat(),
                cost_per_month_usd=100.0,
                kpi_supported="acc >= 0.9",
                notes="",
            ),
            Model(
                id="mod-002",
                name="test-model-b",
                framework="xgboost",
                version="2.0",
                task_type="regression",
                environment="staging",
                owner_team="team-b",
                status="active",
                last_deployed_at=(now - timedelta(days=60)).isoformat(),
                cost_per_month_usd=200.0,
                kpi_supported="rmse < 1.0",
                notes="",
            ),
            Model(
                id="mod-003",
                name="test-model-c",
                framework="pytorch",
                version="3.0",
                task_type="image-classification",
                environment="development",
                owner_team="team-c",
                status="inactive",
                last_deployed_at=(now - timedelta(days=120)).isoformat(),
                cost_per_month_usd=50.0,
                kpi_supported="top5 >= 0.9",
                notes="",
            ),
        ]
        session.add_all(models)

        snapshots = [
            MetricSnapshot(
                model_id="mod-001",
                captured_at=(now - timedelta(hours=1)).isoformat(),
                latency_p95_ms=100.0,
                drift_score=0.01,
                accuracy_score=0.95,
                availability_pct=99.9,
            ),
            MetricSnapshot(
                model_id="mod-001",
                captured_at=(now - timedelta(hours=25)).isoformat(),
                latency_p95_ms=110.0,
                drift_score=0.02,
                accuracy_score=0.94,
                availability_pct=99.8,
            ),
            MetricSnapshot(
                model_id="mod-002",
                captured_at=(now - timedelta(hours=2)).isoformat(),
                latency_p95_ms=200.0,
                drift_score=0.05,
                accuracy_score=0.88,
                availability_pct=97.0,
            ),
        ]
        session.add_all(snapshots)
        session.commit()

    yield
