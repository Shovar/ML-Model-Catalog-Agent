from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from catalogue.schema import MetricSnapshot, Model, get_engine, init_db


def seed(engine=None):
    if engine is None:
        engine = get_engine()
    init_db(engine)

    with Session(engine) as session:
        if session.query(Model).count() > 0:
            print("Database already seeded, skipping.")
            return

        now = datetime.now(timezone.utc)

        models_data = [
            Model(
                id="mod-001",
                name="fraud-detection-v2",
                framework="scikit-learn",
                version="2.1.0",
                task_type="classification",
                environment="production",
                owner_team="risk-analytics",
                status="active",
                last_deployed_at=(now - timedelta(days=5)).isoformat(),
                cost_per_month_usd=450.0,
                kpi_supported="F1-score >= 0.92",
                notes="Main fraud detection model for transaction screening.",
            ),
            Model(
                id="mod-002",
                name="recommendation-engine",
                framework="xgboost",
                version="1.4.2",
                task_type="ranking",
                environment="staging",
                owner_team="personalization",
                status="active",
                last_deployed_at=(now - timedelta(days=2)).isoformat(),
                cost_per_month_usd=320.0,
                kpi_supported="Recall@10 >= 0.85",
                notes="Candidate generation for home feed recommendations.",
            ),
            Model(
                id="mod-003",
                name="sentiment-classifier",
                framework="transformers",
                version="3.0.1",
                task_type="text-classification",
                environment="production",
                owner_team="nlp",
                status="active",
                last_deployed_at=(now - timedelta(days=45)).isoformat(),
                cost_per_month_usd=180.0,
                kpi_supported="Accuracy >= 0.88",
                notes="BERT-based sentiment analysis for customer feedback.",
            ),
            Model(
                id="mod-004",
                name="churn-predictor",
                framework="lightgbm",
                version="1.0.0",
                task_type="classification",
                environment="production",
                owner_team="growth",
                status="decommissioned",
                last_deployed_at=(now - timedelta(days=200)).isoformat(),
                cost_per_month_usd=0.0,
                kpi_supported="AUC >= 0.80",
                notes="Superseded by churn-predictor-v2. Retained for audit.",
            ),
            Model(
                id="mod-005",
                name="image-classifier",
                framework="pytorch",
                version="0.9.0",
                task_type="image-classification",
                environment="development",
                owner_team="cv",
                status="inactive",
                last_deployed_at=(now - timedelta(days=90)).isoformat(),
                cost_per_month_usd=50.0,
                kpi_supported="Top-5 accuracy >= 0.90",
                notes="Prototype for product image tagging. No active development.",
            ),
            Model(
                id="mod-006",
                name="anomaly-detection-stream",
                framework="pytorch",
                version="0.5.0",
                task_type="anomaly-detection",
                environment="staging",
                owner_team="ml-platform",
                status="active",
                last_deployed_at=(now - timedelta(days=60)).isoformat(),
                cost_per_month_usd=210.0,
                kpi_supported="Precision >= 0.95",
                notes="Real-time anomaly detection for streaming metrics.",
            ),
            Model(
                id="mod-007",
                name="pricing-optimizer",
                framework="scikit-learn",
                version="4.2.0",
                task_type="regression",
                environment="production",
                owner_team="pricing",
                status="active",
                last_deployed_at=(now - timedelta(days=1)).isoformat(),
                cost_per_month_usd=600.0,
                kpi_supported="RMSE <= 1.5",
                notes="Dynamic pricing model used across all regions.",
            ),
        ]
        session.add_all(models_data)

        snapshots_data = [
            MetricSnapshot(
                model_id="mod-001",
                captured_at=(now - timedelta(hours=2)).isoformat(),
                latency_p95_ms=145.2,
                drift_score=0.03,
                accuracy_score=0.94,
                availability_pct=99.8,
            ),
            MetricSnapshot(
                model_id="mod-001",
                captured_at=(now - timedelta(hours=26)).isoformat(),
                latency_p95_ms=152.0,
                drift_score=0.02,
                accuracy_score=0.94,
                availability_pct=99.9,
            ),
            MetricSnapshot(
                model_id="mod-002",
                captured_at=(now - timedelta(hours=1)).isoformat(),
                latency_p95_ms=210.5,
                drift_score=0.07,
                accuracy_score=0.83,
                availability_pct=97.2,
            ),
            MetricSnapshot(
                model_id="mod-003",
                captured_at=(now - timedelta(hours=3)).isoformat(),
                latency_p95_ms=320.1,
                drift_score=0.11,
                accuracy_score=0.89,
                availability_pct=99.5,
            ),
            MetricSnapshot(
                model_id="mod-003",
                captured_at=(now - timedelta(hours=48)).isoformat(),
                latency_p95_ms=305.4,
                drift_score=0.09,
                accuracy_score=0.90,
                availability_pct=99.6,
            ),
            MetricSnapshot(
                model_id="mod-005",
                captured_at=(now - timedelta(hours=12)).isoformat(),
                latency_p95_ms=95.3,
                drift_score=0.01,
                accuracy_score=0.76,
                availability_pct=88.0,
            ),
            MetricSnapshot(
                model_id="mod-006",
                captured_at=(now - timedelta(hours=6)).isoformat(),
                latency_p95_ms=180.0,
                drift_score=0.04,
                accuracy_score=0.91,
                availability_pct=99.1,
            ),
            MetricSnapshot(
                model_id="mod-007",
                captured_at=(now - timedelta(minutes=30)).isoformat(),
                latency_p95_ms=88.7,
                drift_score=0.01,
                accuracy_score=0.97,
                availability_pct=99.95,
            ),
        ]
        session.add_all(snapshots_data)
        session.commit()
        print(f"Seeded {len(models_data)} models and {len(snapshots_data)} metric snapshots.")


if __name__ == "__main__":
    seed()
