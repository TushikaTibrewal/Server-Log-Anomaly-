# Server Log Anomaly Detector

## Overview

This project detects anomalous server activity from HTTP server logs. It combines:

1. Feature engineering with Pandas
2. StandardScaler
3. PCA with one component for an activity score
4. KMeans clustering for IP behavior tiers
5. IsolationForest for anomaly detection

The pipeline works at the **per-IP address** level.

## Project Structure

```text
server_log_anomaly_detector/
├── main.py
├── features.py
├── models.py
├── requirements.txt
├── README.md
└── tests/
    └── test_pipeline.py
```

## Expected Input Columns

The script accepts CSV or Excel files. It expects columns equivalent to:

| Required field | Accepted aliases |
|---|---|
| ip_address | ip, client_ip, source_ip, src_ip |
| endpoint | url, path, request, uri |
| response_size | bytes, response_bytes, content_length, size |
| status_code | status, http_status, response_code |
| timestamp | time, datetime, date, request_time |

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py "server_logs.csv"
```

Save output to a specific file:

```bash
python main.py "server_logs.csv" --output results.csv
```

Run without writing output:

```bash
python main.py "server_logs.csv" --dry-run
```

Change clustering and anomaly settings:

```bash
python main.py "server_logs.csv" --clusters 3 --contamination 0.05
```

## Output Columns

- `ip_address`: IP address
- `total_requests`: Total requests made by the IP
- `unique_endpoints`: Number of unique endpoints visited
- `average_response_size`: Average response size
- `error_rate`: Percentage of 4xx and 5xx responses
- `requests_per_minute`: Request rate
- `score`: PCA-based activity score
- `cluster`: KMeans cluster ID
- `tier`: Heavy user, Normal, or Light user
- `is_anomaly`: IsolationForest anomaly flag
- `anomaly_score`: IsolationForest decision score

## Run Tests

```bash
pytest -q
```

## Interpretation

- **Heavy user:** Higher overall activity based on the engineered features.
- **Normal:** Moderate activity relative to other IPs.
- **Light user:** Lower activity relative to other IPs.
- **Anomaly:** An IP whose feature pattern is unusual according to IsolationForest.

The labels are descriptive and should be validated using the actual feature values. An anomaly flag does not automatically mean malicious behavior; it may also indicate a bot, a malfunctioning service, a legitimate traffic spike, or unusual usage.

## Author

Tushika Tibrewal
