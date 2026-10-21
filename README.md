# ML Network Intrusion Detector

> **Project Vertical: Cybersecurity**
> **Sub-Domain: Network Security / Intrusion Detection**
> **Technology: Machine Learning**

---

## Project Overview

The **ML Network Intrusion Detector** is a cybersecurity system that uses Machine Learning to analyze network traffic and classify connections as **NORMAL** or **ATTACK**. It demonstrates how ML can power defensive network security and intrusion detection.

This project is designed as an academic cybersecurity project — not a generic ML exercise. The core problem is a network security problem; ML is the technical solution approach.

---

## Problem Statement

Modern networks face increasingly sophisticated cyber attacks. Traditional signature-based Intrusion Detection Systems (IDS) only detect known attacks using fixed rules. They fail against new, unseen attack patterns and generate excessive false positives.

**This project proposes an ML-based IDS** that learns attack patterns from labeled network traffic data, enabling adaptive detection of both known and unknown intrusions.

---

## Project Objectives

- ✅ Build a Machine Learning based Network Intrusion Detection System
- ✅ Use the NSL-KDD benchmark cybersecurity dataset
- ✅ Train and compare three ML classifiers
- ✅ Evaluate using Accuracy, Precision, Recall, F1-Score
- ✅ Save the best performing model
- ✅ Deploy a web application for real-time prediction
- ✅ Support binary classification: NORMAL vs ATTACK

---

## Features

- 🔍 **Manual Prediction** — Enter 41 network features for instant classification
- 📁 **Batch Prediction** — Upload CSV file for bulk traffic analysis
- 📊 **Model Performance** — View real accuracy, confusion matrix, feature importance
- 🤖 **3 ML Models** — Logistic Regression, Decision Tree, Random Forest
- 🌐 **Web Interface** — Professional cybersecurity-themed Flask application
- 💾 **Model Persistence** — Best model saved and reloaded automatically

---

## Dataset: NSL-KDD

| Property | Value |
|----------|-------|
| Name | NSL-KDD |
| Source | Canadian Institute for Cybersecurity |
| Features | 41 network traffic features |
| Target | `label` — normal / attack |
| Task | Binary Classification |
| This project | Synthetic NSL-KDD-like dataset |

**Feature Categories:**
- Basic features: `duration`, `protocol_type`, `service`, `flag`, `src_bytes`, `dst_bytes`, ...
- Content features: `hot`, `num_failed_logins`, `logged_in`, `num_compromised`, ...
- Traffic features: `count`, `serror_rate`, `same_srv_rate`, ...
- Host-based features: `dst_host_count`, `dst_host_serror_rate`, ...

---

## Technologies Used

| Category | Technology |
|----------|-----------|
| Language | Python 3.8+ |
| ML Framework | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Web Framework | Flask |
| Model Storage | Joblib |

---

## Project Structure

```
ML-Network-Intrusion-Detector/
│
├── data/
│   ├── README.md               ← Dataset documentation
│   └── processed_data.csv      ← Generated after training
│
├── models/
│   ├── README.md               ← Model documentation
│   ├── best_model.pkl          ← Saved best ML model
│   ├── scaler.pkl              ← Fitted StandardScaler
│   ├── label_encoder.pkl       ← Label encoder
│   ├── feature_encoders.pkl    ← Categorical feature encoders
│   └── model_results.json      ← Performance metrics
│
├── results/
│   ├── README.md               ← Results documentation
│   ├── model_comparison.csv    ← All model metrics
│   ├── confusion_matrix.png    ← Best model confusion matrix
│   ├── feature_importance.png  ← RF feature importance
│   ├── model_accuracy.png      ← Model comparison chart
│   └── classification_report.txt
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py   ← Data cleaning & preprocessing
│   ├── train_model.py          ← ML model training
│   ├── evaluate_model.py       ← Model evaluation
│   └── predict.py              ← Prediction functions
│
├── templates/                  ← Flask HTML templates
│   ├── base.html
│   ├── home.html
│   ├── predict.html
│   ├── performance.html
│   ├── about.html
│   └── 404.html
│
├── app.py                      ← Flask web application
├── requirements.txt            ← Python dependencies
├── README.md                   ← This file
└── .gitignore
```

---

## Installation & Setup

### 1. Clone / Download the Project

```bash
cd ML-Network-Intrusion-Detector
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## Model Training

Run the training pipeline (generates synthetic data, trains models, saves results):

```bash
python src/train_model.py
```

**What this does:**
1. Generates a synthetic NSL-KDD-like dataset (15,000 records)
2. Cleans and preprocesses the data
3. Encodes categorical features
4. Splits into 80% train / 20% test
5. Trains Logistic Regression, Decision Tree, Random Forest
6. Evaluates all models and prints real metrics
7. Saves best model to `models/best_model.pkl`
8. Saves confusion matrix, feature importance, comparison charts to `results/`

---

## Running the Web Application

```bash
python app.py
```

Open browser: **http://127.0.0.1:5000**

> ⚠️ Train the model first before running the web app.

---

## Prediction

### Manual Prediction (Web UI)
1. Go to **http://127.0.0.1:5000/predict**
2. Enter network connection features (or load a sample)
3. Click **Classify Network Traffic**
4. View **NORMAL** or **ATTACK** result with confidence

### Batch Prediction (CSV Upload)
1. Prepare a CSV with NSL-KDD format columns
2. Upload at **http://127.0.0.1:5000/predict**
3. View prediction for each record + summary statistics

### Command Line Prediction
```bash
python src/predict.py
```

### API Prediction
```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"duration":5,"protocol_type":"tcp","service":"http","flag":"SF","src_bytes":2300,"dst_bytes":4500}'
```

---

## Model Evaluation

View results at: **http://127.0.0.1:5000/performance**

Results include (actual values after training):
- Accuracy, Precision, Recall, F1-Score for each model
- Confusion Matrix of the best model
- Feature Importance (Random Forest)
- Model Comparison Chart

---

## Results

> Results are generated by actual model training. Run `python src/train_model.py` to see real numbers.
> Do NOT use any pre-filled/fabricated numbers from external sources.

Results are saved to:
- `results/model_comparison.csv`
- `results/confusion_matrix.png`
- `results/feature_importance.png`
- `results/model_accuracy.png`
- `results/classification_report.txt`
- `models/model_results.json`

---

## Limitations

- Uses synthetic NSL-KDD-like data (not real network traffic captures)
- Binary classification only (Normal vs Attack — not attack type)
- May not generalize to entirely unseen attack types
- Requires retraining as new attack patterns emerge
- Not a production-ready IDS (no live network tap integration)

---

## Future Scope

- Multi-class classification (DoS, Probe, R2L, U2R attack types)
- Integration with real-time network monitoring (Scapy, Zeek, Suricata)
- Deep learning models (LSTM for temporal traffic patterns)
- Automated retraining pipeline with drift detection
- Real CIC-IDS2017 dataset integration
- Alert dashboard with email/webhook notifications

---

## Safety Notice

> 🔒 This is a **defensive cybersecurity project** only.
> It detects intrusions — it does NOT implement attacks, exploits, malware,
> unauthorized scanning, or any offensive capabilities.
> Use only with authorized network data.

---

## Conclusion

This project demonstrates how Machine Learning can be applied to the cybersecurity problem of Network Intrusion Detection. By training classifiers on labeled network traffic data, the system can automatically identify malicious connections, supporting network defenders in protecting their infrastructure.

**Project Vertical: Cybersecurity | Sub-Domain: Network Security / Intrusion Detection | Technology: Machine Learning**
