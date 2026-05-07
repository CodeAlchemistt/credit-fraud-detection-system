"""
Tritiya Fraud Detection System — Flask Backend
====================================================
Entry point for the web application. Handles routing and
the core fraud-detection prediction endpoint.

Usage:
    pip install flask pandas numpy scikit-learn mysql-connector-python
    python app.py
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import json
import random
import time

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Fraud Detection Logic
# ---------------------------------------------------------------------------
# REPLACE this stub with your real trained model:
#
#   import joblib
#   model = joblib.load("ml/fraud_model.pkl")
#   scaler = joblib.load("ml/scaler.pkl")
#
# Then replace `mock_predict()` with:
#   scaled = scaler.transform([[amount, v1, v2, v3, v4, v5]])
#   prob   = model.predict_proba(scaled)[0][1]
# ---------------------------------------------------------------------------

FRAUD_THRESHOLD = 0.50   # probability cutoff — tune to your model

def mock_predict(amount: float, features: list[float]) -> dict:
    """
    Stub predictor. Produces a realistic-looking probability score
    from the raw feature values so the UI works end-to-end.
    Delete this once you load your real model.
    """
    # Heuristic: large amounts + extreme V-values push fraud probability up
    feature_signal = sum(abs(f) for f in features) / (len(features) or 1)
    raw = (amount / 5000) * 0.4 + (feature_signal / 10) * 0.6
    prob = min(max(raw + random.gauss(0, 0.05), 0.0), 1.0)
    return {
        "fraud_probability": round(prob, 4),
        "is_fraud": prob >= FRAUD_THRESHOLD,
        "risk_score": int(prob * 100),
    }


# ---------------------------------------------------------------------------
# Page Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")


@app.route("/about")
def about():
    return render_template("about.html")


# ---------------------------------------------------------------------------
# API — Prediction Endpoint
# ---------------------------------------------------------------------------

@app.route("/api/predict", methods=["POST"])
def predict():
    """
    Accepts JSON: { amount, v1..v5, merchant, card_type }
    Returns JSON with prediction results + echoed transaction data.
    """
    try:
        data = request.get_json(force=True)

        amount   = float(data.get("amount", 0))
        features = [float(data.get(f"v{i}", 0)) for i in range(1, 6)]
        merchant  = data.get("merchant", "Unknown Merchant")
        card_type = data.get("card_type", "Visa")

        # ── Simulate model latency (remove in production) ──
        time.sleep(0.8)

        result = mock_predict(amount, features)

        # ── Build enriched response ──
        response = {
            "success": True,
            "transaction": {
                "id":          f"TXN-{random.randint(100000, 999999)}",
                "amount":      round(amount, 2),
                "merchant":    merchant,
                "card_type":   card_type,
                "timestamp":   time.strftime("%Y-%m-%d %H:%M:%S"),
                "features":    {f"V{i+1}": features[i] for i in range(len(features))},
            },
            "prediction": result,
        }

        return jsonify(response), 200

    except Exception as exc:
        return jsonify({"success": False, "error": str(exc)}), 400


# ---------------------------------------------------------------------------
# API — Analytics Stats (mock data; swap for real DB queries)
# ---------------------------------------------------------------------------

@app.route("/api/stats")
def stats():
    return jsonify({
        "total_transactions": 284_807,
        "fraud_cases":        492,
        "fraud_rate":         0.00173,
        "model_accuracy":     0.9994,
        "precision":          0.937,
        "recall":             0.872,
        "f1_score":           0.903,
        "auc_roc":            0.9825,
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
