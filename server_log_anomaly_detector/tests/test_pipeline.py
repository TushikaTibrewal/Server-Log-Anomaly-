import pandas as pd

from features import engineer_features
from models import run_pipeline


def sample_logs():
    return pd.DataFrame(
        {
            "ip_address": [
                "10.0.0.1", "10.0.0.1", "10.0.0.2",
                "10.0.0.2", "10.0.0.3", "10.0.0.3",
                "10.0.0.4", "10.0.0.4", "10.0.0.5",
                "10.0.0.5", "10.0.0.6", "10.0.0.6",
            ],
            "endpoint": [
                "/home", "/login", "/home", "/api",
                "/home", "/home", "/admin", "/admin",
                "/api", "/api", "/health", "/health",
            ],
            "response_size": [
                100, 200, 150, 200, 100, 100,
                9000, 9500, 120, 130, 110, 120,
            ],
            "status_code": [
                200, 200, 200, 404, 200, 500,
                500, 503, 200, 200, 200, 200,
            ],
            "timestamp": pd.date_range(
                "2026-01-01", periods=12, freq="min"
            ),
        }
    )


def test_feature_engineering_columns():
    features = engineer_features(sample_logs())

    expected = {
        "ip_address",
        "total_requests",
        "unique_endpoints",
        "average_response_size",
        "error_rate",
        "requests_per_minute",
    }

    assert expected.issubset(set(features.columns))
    assert len(features) == 6


def test_pipeline_runs_on_sample_data():
    features = engineer_features(sample_logs())
    result, metadata = run_pipeline(
        features,
        n_clusters=3,
        contamination=0.2,
    )

    assert len(result) == len(features)
    assert "score" in result.columns
    assert "tier" in result.columns
    assert "is_anomaly" in result.columns
    assert "explained_variance" in metadata


def test_anomaly_flags_are_boolean():
    features = engineer_features(sample_logs())
    result, _ = run_pipeline(
        features,
        n_clusters=3,
        contamination=0.2,
    )

    assert result["is_anomaly"].dtype == bool
