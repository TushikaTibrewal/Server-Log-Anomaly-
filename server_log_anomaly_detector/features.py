import pandas as pd
import numpy as np


COLUMN_ALIASES = {
    "ip_address": ["ip_address", "ip", "client_ip", "source_ip", "src_ip", "remote_addr"],
    "endpoint": ["endpoint", "url", "path", "request", "uri"],
    "response_size": ["response_size", "bytes", "response_bytes", "content_length", "size"],
    "status_code": ["status_code", "status", "http_status", "response_code"],
    "timestamp": ["timestamp", "time", "datetime", "date", "request_time"],
}


def _find_column(df, aliases):
    normalized = {str(c).strip().lower(): c for c in df.columns}
    for alias in aliases:
        if alias in normalized:
            return normalized[alias]
    return None


def _standardize_columns(df):
    result = df.copy()

    for target, aliases in COLUMN_ALIASES.items():
        source = _find_column(result, aliases)
        if source is not None:
            result[target] = result[source]

    required = ["ip_address", "endpoint", "response_size", "status_code", "timestamp"]
    missing = [col for col in required if col not in result.columns]

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing)
            + ". Expected aliases include: "
            + ", ".join(required)
        )

    result["ip_address"] = result["ip_address"].astype(str)
    result["endpoint"] = result["endpoint"].astype(str)
    result["response_size"] = pd.to_numeric(
        result["response_size"], errors="coerce"
    ).fillna(0)
    result["status_code"] = pd.to_numeric(
        result["status_code"], errors="coerce"
    )
    result["timestamp"] = pd.to_datetime(
        result["timestamp"], errors="coerce"
    )

    result = result.dropna(
        subset=["ip_address", "timestamp", "status_code"]
    )

    return result


def engineer_features(df):
    """Create one feature row per IP address."""
    data = _standardize_columns(df)

    if data.empty:
        raise ValueError("No valid log rows remain after cleaning.")

    data["is_error"] = data["status_code"].between(400, 599).astype(int)

    time_span_minutes = (
        (data["timestamp"].max() - data["timestamp"].min()).total_seconds()
        / 60
    )
    time_span_minutes = max(time_span_minutes, 1.0)

    grouped = data.groupby("ip_address")

    feature_df = grouped.agg(
        total_requests=("ip_address", "size"),
        unique_endpoints=("endpoint", "nunique"),
        average_response_size=("response_size", "mean"),
        error_rate=("is_error", "mean"),
        first_seen=("timestamp", "min"),
        last_seen=("timestamp", "max"),
    ).reset_index()

    feature_df["requests_per_minute"] = (
        feature_df["total_requests"] / time_span_minutes
    )

    feature_df["error_rate"] = feature_df["error_rate"] * 100

    feature_df = feature_df[
        [
            "ip_address",
            "total_requests",
            "unique_endpoints",
            "average_response_size",
            "error_rate",
            "requests_per_minute",
        ]
    ]

    return feature_df
