"""
app.py
======
ML Network Intrusion Detector — Cybersecurity Web Application
Domain : Network Security / Intrusion Detection
Technology : Machine Learning + Flask

Routes:
  GET  /           → Home page
  GET  /predict    → Prediction form (manual input)
  POST /predict    → Run prediction on submitted form data
  POST /upload     → Batch CSV prediction
  GET  /performance → Model performance page
  GET  /about      → About page
  GET  /api/predict → JSON API endpoint
"""

import os
import io
import json
import traceback
import numpy as np
import pandas as pd
from flask import (Flask, render_template, request, jsonify,
                   redirect, url_for, flash, send_from_directory)
from werkzeug.utils import secure_filename
import warnings
warnings.filterwarnings('ignore')

# ── App setup ─────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = 'mlids_cybersecurity_2024_secret'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024   # 16 MB upload limit
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'csv'}

# ── Import prediction module ───────────────────────────────
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.predict import (predict_single, predict_csv,
                          get_sample_normal, get_sample_attack,
                          FEATURE_NAMES)
from src.evaluate_model import get_model_results

MODELS_READY = os.path.exists(os.path.join('models', 'best_model.pkl'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_performance_data():
    """Load actual model results from JSON."""
    data = get_model_results()
    if not data:
        return None
    # Load confusion matrix image as base64 for embedding
    cm_path  = os.path.join('results', 'confusion_matrix.png')
    acc_path = os.path.join('results', 'model_accuracy.png')
    fi_path  = os.path.join('results', 'feature_importance.png')
    import base64
    def img_b64(path):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        return None
    data['cm_img']  = img_b64(cm_path)
    data['acc_img'] = img_b64(acc_path)
    data['fi_img']  = img_b64(fi_path)
    return data


# ── Routes ────────────────────────────────────────────────

@app.route('/')
def home():
    perf = get_performance_data()
    return render_template('home.html',
                           models_ready=MODELS_READY,
                           perf=perf)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    result     = None
    error      = None
    form_data  = {}
    sample_mode = request.args.get('sample', '')

    # Pre-fill with sample data if requested
    if sample_mode == 'normal' and request.method == 'GET':
        form_data = get_sample_normal()
    elif sample_mode == 'attack' and request.method == 'GET':
        form_data = get_sample_attack()

    if request.method == 'POST':
        try:
            if not MODELS_READY:
                raise RuntimeError("Model not trained yet. Run 'python src/train_model.py'.")

            # Collect form values
            input_dict = {}
            for feat in FEATURE_NAMES:
                val = request.form.get(feat, '0')
                form_data[feat] = val
                try:
                    input_dict[feat] = float(val)
                except ValueError:
                    input_dict[feat] = val   # categorical: pass as string

            result = predict_single(input_dict)

        except Exception as e:
            error = str(e)
            app.logger.error(traceback.format_exc())

    return render_template('predict.html',
                           result=result,
                           error=error,
                           form_data=form_data,
                           feature_names=FEATURE_NAMES,
                           models_ready=MODELS_READY)


@app.route('/upload', methods=['POST'])
def upload():
    error    = None
    summary  = None
    rows     = None

    try:
        if not MODELS_READY:
            raise RuntimeError("Model not trained yet. Run 'python src/train_model.py'.")

        if 'csv_file' not in request.files:
            raise ValueError("No file provided.")

        file = request.files['csv_file']
        if file.filename == '':
            raise ValueError("No file selected.")

        if not allowed_file(file.filename):
            raise ValueError("Only CSV files are supported.")

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        df_result, summary = predict_csv(filepath)
        rows = df_result.head(50).to_dict(orient='records')   # show first 50

    except Exception as e:
        error = str(e)
        app.logger.error(traceback.format_exc())

    return render_template('predict.html',
                           upload_result=rows,
                           upload_summary=summary,
                           error=error,
                           form_data={},
                           feature_names=FEATURE_NAMES,
                           models_ready=MODELS_READY)


@app.route('/performance')
def performance():
    perf = get_performance_data()
    if not perf and MODELS_READY:
        flash("Performance data not available. Re-run training.", "warning")
    return render_template('performance.html',
                           perf=perf,
                           models_ready=MODELS_READY)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """JSON API endpoint for programmatic prediction."""
    try:
        if not MODELS_READY:
            return jsonify({'error': 'Model not trained. Run train_model.py first.'}), 503

        data = request.get_json(force=True)
        if not data:
            return jsonify({'error': 'No JSON data provided.'}), 400

        result = predict_single(data)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status')
def api_status():
    """Health check endpoint."""
    perf = get_model_results()
    return jsonify({
        'status':       'running',
        'models_ready': MODELS_READY,
        'best_model':   perf.get('best_model_name', 'N/A') if perf else 'N/A',
        'accuracy':     perf.get('accuracy', 'N/A') if perf else 'N/A',
    })


# ── Error handlers ─────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(413)
def too_large(e):
    flash("File too large. Maximum size is 16MB.", "danger")
    return redirect(url_for('predict'))


# ── Main ───────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 60)
    print("  ML NETWORK INTRUSION DETECTOR")
    print("  Cybersecurity Web Application")
    print("  http://127.0.0.1:5000")
    print("=" * 60)
    if not MODELS_READY:
        print("\n  [WARNING] Model not found.")
        print("  Run: python src/train_model.py")
        print("  Then restart this application.\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
