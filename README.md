
# 🚨 Server Log Anomaly Detector

## 📌 Project Overview

The **Server Log Anomaly Detector** is a Machine Learning project that identifies unusual server activity from HTTP server logs.

The project combines **StandardScaler, PCA, KMeans, and IsolationForest** to analyze server traffic at the IP address level.

The system engineers behavioral features for each IP address, assigns activity tiers, and flags potentially anomalous activity.

---

## 🎯 Objectives

- Load server log data using Pandas.
- Engineer per-IP behavioral features.
- Normalize features using StandardScaler.
- Apply PCA with one component to generate an activity score.
- Use KMeans clustering to classify IP behavior.
- Apply IsolationForest to detect anomalous activity.
- Produce a final DataFrame with IP addresses, scores, tiers, and anomaly flags.
- Structure the project as a modular Python application.
- Add CLI arguments, logging, and unit tests.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Pandas | Data loading and feature engineering |
| NumPy | Numerical operations |
| Scikit-learn | Machine Learning |
| StandardScaler | Feature normalization |
| PCA | Dimensionality reduction |
| KMeans | IP behavior clustering |
| IsolationForest | Anomaly detection |
| Pytest | Unit testing |

---

## 🔄 Machine Learning Pipeline

```text
Server Log Dataset
        |
        ▼
Data Loading
        |
        ▼
Feature Engineering
        |
        ▼
StandardScaler
        |
        ▼
PCA (1 Component)
        |
        ▼
Per-IP Activity Score
        |
        ▼
KMeans Clustering
        |
        ▼
IP Behavior Tiers
        |
        ▼
IsolationForest
        |
        ▼
Anomaly Detection
        |
        ▼
Final Results CSV
```

---

## 📂 Project Structure

```text
server_log_anomaly_detector/
│
├── main.py
├── features.py
├── models.py
├── requirements.txt
├── README.md
│
├── sample_server_logs.csv
│
└── tests/
    └── test_pipeline.py
```

### File Description

| File | Description |
|---|---|
| `main.py` | Entry point, CLI arguments, and logging |
| `features.py` | Feature engineering functions |
| `models.py` | Scaler, PCA, KMeans, and IsolationForest pipeline |
| `requirements.txt` | Required Python libraries |
| `test_pipeline.py` | Unit tests using Pytest |
| `sample_server_logs.csv` | Sample server log dataset |

---

## 📊 Dataset

The project supports HTTP server log datasets, including the **HTTP CSIC 2010 dataset** or synthetic server logs.

The input dataset should contain information about server requests, IP addresses, endpoints, response sizes, status codes, and timestamps.

### Required Input Columns

| Column | Description |
|---|---|
| `ip_address` | Client IP address |
| `endpoint` | Requested URL or endpoint |
| `response_size` | Size of the HTTP response |
| `status_code` | HTTP response status code |
| `timestamp` | Date and time of the request |

The feature engineering module also accepts several common column aliases.

---

## ⚙️ Feature Engineering

Features are calculated per IP address.

| Feature | Description |
|---|---|
| `total_requests` | Total number of requests |
| `unique_endpoints` | Number of distinct endpoints accessed |
| `average_response_size` | Average response size |
| `error_rate` | Percentage of 4xx and 5xx responses |
| `requests_per_minute` | Request rate over the observed log period |

### Error Rate

```text
Error Rate =
(Number of 4xx and 5xx responses / Total requests) × 100
```

---

## 🧠 Machine Learning Methodology

### 1. StandardScaler

Normalizes the engineered features so they have comparable scales.

### 2. PCA

PCA with one component is used to calculate a per-IP activity score.

The score summarizes variation across the standardized features. It is not a guaranteed measure of maliciousness.

### 3. KMeans

KMeans groups IP addresses into three behavioral tiers:

- Heavy user
- Normal
- Light user

These tiers are based on relative activity and should be interpreted using the actual cluster statistics.

### 4. IsolationForest

IsolationForest identifies IP addresses with unusual feature patterns.

The anomaly flag is:

```python
is_anomaly = True
```

when the model classifies an IP as an outlier.

An anomaly does not automatically mean an attack. It may indicate legitimate traffic spikes, bots, system failures, or other unusual activity.

---

## 🚀 Installation

### Step 1: Navigate to the project folder

Open the VS Code terminal:

```powershell
cd "C:\Users\tushi\OneDrive\Documents\AWS\Week 5\server_log_anomaly_detector"
```

If your folder is located elsewhere, update the path accordingly.

### Step 2: Install dependencies

```powershell
pip install -r requirements.txt
```

---

## ▶️ How to Run

### Run with sample data

```powershell
python main.py sample_server_logs.csv
```

### Run with your own dataset

```powershell
python main.py "path\to\server_logs.csv"
```

### Save output to a custom location

```powershell
python main.py sample_server_logs.csv --output results.csv
```

### Run in dry-run mode

The dry-run option prints the flagged anomalies without writing an output file.

```powershell
python main.py sample_server_logs.csv --dry-run
```

### Customize clustering and anomaly detection

```powershell
python main.py sample_server_logs.csv --clusters 3 --contamination 0.05
```

---

## 📤 Output

The pipeline produces a CSV containing:

| Column | Description |
|---|---|
| `ip_address` | IP address |
| `total_requests` | Total requests |
| `unique_endpoints` | Distinct endpoints |
| `average_response_size` | Average response size |
| `error_rate` | Error percentage |
| `requests_per_minute` | Request rate |
| `score` | PCA-based activity score |
| `cluster` | KMeans cluster ID |
| `tier` | Behavioral tier |
| `is_anomaly` | Anomaly flag |
| `anomaly_score` | IsolationForest decision score |

---

## 🧪 Unit Testing

The project includes three unit tests:

1. Verify that feature engineering produces the required columns.
2. Verify that the complete pipeline runs on sample data.
3. Verify that anomaly flags are Boolean values.

Run the tests:

```powershell
pytest -q
```

---

## 💼 Business Applications

This project can be used to support:

- Server monitoring
- Unusual traffic detection
- Bot activity analysis
- Error-rate monitoring
- Security investigation
- Operational anomaly detection

The output should be reviewed alongside server context and security monitoring systems before taking action.

---

## 🔮 Future Improvements

- Add time-windowed features such as requests per minute per hour.
- Include HTTP methods, user agents, and response status distributions.
- Add visual dashboards using Power BI or Streamlit.
- Tune the IsolationForest contamination parameter.
- Compare KMeans with DBSCAN and other clustering methods.
- Train and persist models for consistent future scoring.
- Add automated alerts for high-priority anomalies.

---

## 👩‍💻 Author

**Tushika Tibrewal**

B.Tech – Data Science and Business Systems  
SRM Institute of Science and Technology

---

## ⭐ Acknowledgements

- Scikit-learn Documentation
- Pandas Documentation
- HTTP CSIC 2010 Dataset (if used)
