import argparse
import logging
from pathlib import Path

import pandas as pd

from features import engineer_features
from models import run_pipeline


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )


def load_data(file_path):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)

    if path.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(path)

    raise ValueError("Supported input formats are CSV, XLSX, and XLS.")


def main():
    parser = argparse.ArgumentParser(
        description="Detect anomalous server activity per IP address."
    )

    parser.add_argument(
        "file_path",
        help="Path to the server log CSV or Excel file.",
    )

    parser.add_argument(
        "--output",
        default="server_anomaly_results.csv",
        help="Output CSV path.",
    )

    parser.add_argument(
        "--clusters",
        type=int,
        default=3,
        help="Number of KMeans clusters.",
    )

    parser.add_argument(
        "--contamination",
        type=float,
        default=0.05,
        help="Expected proportion of anomalies, between 0 and 0.5.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print results without writing an output file.",
    )

    args = parser.parse_args()
    configure_logging()

    if not 0 < args.contamination <= 0.5:
        raise ValueError("--contamination must be > 0 and <= 0.5.")

    logging.info("Loading data from %s", args.file_path)
    raw_df = load_data(args.file_path)
    logging.info("Loaded %d rows", len(raw_df))

    feature_df = engineer_features(raw_df)
    logging.info("Engineered features for %d IPs", len(feature_df))

    result_df, metadata = run_pipeline(
        feature_df,
        n_clusters=args.clusters,
        contamination=args.contamination,
    )

    logging.info(
        "PCA explained variance: %.4f",
        metadata["explained_variance"],
    )

    anomaly_count = int(result_df["is_anomaly"].sum())
    logging.info("Flagged %d anomalies", anomaly_count)

    flagged = result_df[result_df["is_anomaly"]].sort_values(
        by="anomaly_score"
    )

    print("\nFlagged anomalies:")
    if flagged.empty:
        print("No anomalies were flagged.")
    else:
        print(flagged.to_string(index=False))

    if not args.dry_run:
        result_df.to_csv(args.output, index=False)
        logging.info("Saved results to %s", args.output)


if __name__ == "__main__":
    main()
