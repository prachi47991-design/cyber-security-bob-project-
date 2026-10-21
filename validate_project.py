import sys, json, os
sys.path.insert(0,'.')

# Test 1: All model files exist
print("=== FILE CHECK ===")
files = [
    'models/best_model.pkl','models/scaler.pkl','models/label_encoder.pkl',
    'models/feature_encoders.pkl','models/model_results.json',
    'results/confusion_matrix.png','results/model_accuracy.png',
    'results/feature_importance.png','results/model_comparison.csv',
    'results/classification_report.txt','data/processed_data.csv',
    'Project_Report_ML_Network_Intrusion_Detector.docx'
]
all_ok = True
for f in files:
    status = 'OK' if os.path.exists(f) else 'MISSING'
    if status == 'MISSING':
        all_ok = False
    print(f"  [{status}] {f}")

# Test 2: Prediction accuracy
print("\n=== PREDICTION TEST ===")
from src.predict import predict_single, get_sample_normal, get_sample_attack
r1 = predict_single(get_sample_normal())
r2 = predict_single(get_sample_attack())
t1 = "PASS" if r1["label"] == "NORMAL" else "FAIL"
t2 = "PASS" if r2["label"] == "ATTACK" else "FAIL"
print(f"  [TEST] Normal -> {r1['label']} ({r1['confidence']}%) : {t1}")
print(f"  [TEST] Attack -> {r2['label']} ({r2['confidence']}%) : {t2}")

# Test 3: Flask routes
print("\n=== WEB APP TEST ===")
import app as flask_app
with flask_app.app.test_client() as c:
    routes = [
        ('/', 'Home'),
        ('/predict', 'Predict'),
        ('/performance', 'Performance'),
        ('/about', 'About'),
        ('/api/status', 'API Status')
    ]
    for route, name in routes:
        r = c.get(route)
        status = "PASS" if r.status_code == 200 else "FAIL"
        print(f"  [TEST] GET {route} ({name}): HTTP {r.status_code} : {status}")

# Test 4: Results data
print("\n=== ACTUAL RESULTS ===")
from src.evaluate_model import get_model_results
d = get_model_results()
print(f"  Best Model : {d['best_model_name']}")
print(f"  Accuracy   : {d['accuracy']}%")
print(f"  Precision  : {d['precision']}%")
print(f"  Recall     : {d['recall']}%")
print(f"  F1-Score   : {d['f1_score']}%")

print("\n=== SUMMARY ===")
print(f"  All files present: {all_ok}")
print(f"  Predictions correct: {t1 == 'PASS' and t2 == 'PASS'}")
