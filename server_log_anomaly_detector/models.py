import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "total_requests",
    "unique_endpoints",
    "average_response_size",
    "error_rate",
    "requests_per_minute",
]


def run_pipeline(feature_df, n_clusters=3, contamination=0.05):
    """Run Scaler -> PCA -> KMeans -> IsolationForest."""
    if feature_df.empty:
        raise ValueError("Feature DataFrame is empty.")

    X = feature_df[FEATURE_COLUMNS].copy()
    X = X.replace([np.inf, -np.inf], np.nan).fillna(0)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=1)
    activity_scores = pca.fit_transform(X_scaled).ravel()

    # Make higher scores generally represent more activity.
    activity_idx = [
        FEATURE_COLUMNS.index("total_requests"),
        FEATURE_COLUMNS.index("requests_per_minute"),
    ]

    if pca.components_[0, activity_idx].mean() < 0:
        activity_scores = -activity_scores

    cluster_count = min(n_clusters, len(feature_df))
    if cluster_count < 1:
        raise ValueError("At least one data row is required.")

    kmeans = KMeans(
        n_clusters=cluster_count,
        random_state=42,
        n_init=10,
    )
    clusters = kmeans.fit_predict(X_scaled)

    # Rank clusters by their average activity score.
    cluster_score_means = pd.Series(activity_scores).groupby(clusters).mean()
    ordered_clusters = cluster_score_means.sort_values(
        ascending=False
    ).index.tolist()

    tier_names = ["Heavy user", "Normal", "Light user"]
    tier_map = {}

    for rank, cluster_id in enumerate(ordered_clusters):
        if rank < len(tier_names):
            tier_map[cluster_id] = tier_names[rank]
        else:
            tier_map[cluster_id] = f"Group {rank + 1}"

    isolation_forest = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=200,
    )
    anomaly_predictions = isolation_forest.fit_predict(X_scaled)
    anomaly_scores = isolation_forest.decision_function(X_scaled)

    result = feature_df.copy()
    result["score"] = activity_scores
    result["cluster"] = clusters
    result["tier"] = [tier_map[c] for c in clusters]
    result["is_anomaly"] = anomaly_predictions == -1
    result["anomaly_score"] = anomaly_scores

    explained_variance = float(pca.explained_variance_ratio_[0])

    metadata = {
        "scaler": scaler,
        "pca": pca,
        "kmeans": kmeans,
        "isolation_forest": isolation_forest,
        "explained_variance": explained_variance,
    }

    return result, metadata
