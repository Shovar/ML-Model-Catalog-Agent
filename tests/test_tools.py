from app.tools import get_latency_metrics, get_model_status, list_stale_models


class TestGetModelStatus:
    def test_existing_model(self, db_session):
        result = get_model_status("mod-001")
        assert result["id"] == "mod-001"
        assert result["name"] == "test-model-a"
        assert result["framework"] == "scikit-learn"
        assert result["environment"] == "production"
        assert result["owner_team"] == "team-a"
        assert result["status"] == "active"
        assert result["cost_per_month_usd"] == 100.0

    def test_missing_model(self, db_session):
        result = get_model_status("mod-999")
        assert "error" in result
        assert "not found" in result["error"]


class TestListStaleModels:
    def test_default_threshold_returns_only_old_models(self, db_session):
        result = list_stale_models(threshold_days=30)
        ids = [m["id"] for m in result]
        assert "mod-001" not in ids
        assert "mod-002" in ids
        assert "mod-003" in ids

    def test_custom_threshold_captures_none(self, db_session):
        result = list_stale_models(threshold_days=200)
        assert result == []

    def test_custom_threshold_captures_all(self, db_session):
        result = list_stale_models(threshold_days=1)
        assert len(result) == 3

    def test_response_shape(self, db_session):
        result = list_stale_models(threshold_days=30)
        for item in result:
            assert "id" in item
            assert "name" in item
            assert "environment" in item
            assert "status" in item
            assert "last_deployed_at" in item


class TestGetLatencyMetrics:
    def test_returns_recent_snapshots(self, db_session):
        result = get_latency_metrics("mod-001", hours=24)
        assert result["model_id"] == "mod-001"
        assert result["model_name"] == "test-model-a"
        assert result["lookback_hours"] == 24
        assert len(result["snapshots"]) == 1
        assert result["snapshots"][0]["latency_p95_ms"] == 100.0

    def test_larger_lookback_includes_older_snapshots(self, db_session):
        result = get_latency_metrics("mod-001", hours=48)
        assert len(result["snapshots"]) == 2

    def test_missing_model(self, db_session):
        result = get_latency_metrics("mod-999", hours=24)
        assert "error" in result

    def test_snapshot_shape(self, db_session):
        result = get_latency_metrics("mod-001", hours=24)
        snap = result["snapshots"][0]
        assert "captured_at" in snap
        assert "latency_p95_ms" in snap
        assert "drift_score" in snap
        assert "accuracy_score" in snap
        assert "availability_pct" in snap
