import os
import pickle
import numpy as np
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)  # Agar cross-origin ka issue ho toh handle karne ke liye

# Memory-based temporary history storage (Database ka substitute)
SIMULATED_HISTORY = [
    {
        "transaction": {"id": 1, "amount": 885.0, "merchant": "Amazon"},
        "prediction": {"is_fraud": False, "risk_score": 12}
    },
    {
        "transaction": {"id": 2, "amount": 2500.0, "merchant": "Unknown Merchant"},
        "prediction": {"is_fraud": True, "risk_score": 88}
    }
]

# --- ML MODEL LOADING CONTINGENCY ---
# Aapke project me jahan bhi model load ho raha hai, use safe rakhne ke liye:
try:
    # Agar aapke model ka path alag hai (jaise 'models/fraud_model.pkl'), toh use yahan sahi karein
    model_path = os.path.join(os.path.dirname(__file__), 'models', 'fraud_model.pkl')
    if not os.path.exists(model_path):
        model_path = 'fraud_model.pkl' # fallback to current dir
        
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    print("ML Model Loaded Successfully!")
except Exception as e:
    print(f"Model Loading Warning: {e}. Using rule-based simulation.")
    model = None


# --- MAIN ROUTES ---

@app.route("/")
def index():
    # Aapka main dashboard template render karega
    return render_template("index.html")


@app.route("/api/predict", methods=["POST"])
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json() or request.form
        if not data:
            return jsonify({"success": False, "error": "No data received"})

        # Front-end se data extract karna
        amount = float(data.get("amount", 0))
        merchant = data.get("merchant", "Unknown Merchant")
        
        # ML Model se prediction generate karna
        if model:
            # Apne model ke features ke hisab se array format set karein
            # Yeh ek general structure hai, ise apne dataset ke features ke anusaar adjust karein
            features = np.array([[amount]]) 
            prediction_class = int(model.predict(features)[0])
            risk_score = int(model.predict_proba(features)[0][1] * 100) if hasattr(model, "predict_proba") else (85 if prediction_class == 1 else 15)
        else:
            # Rule-based fallback agar model load na ho paye (Simulation)
            prediction_class = 1 if amount > 2000 else 0
            risk_score = 88 if prediction_class == 1 else 12

        # Naye transaction ko history list me upar add karna
        new_id = len(SIMULATED_HISTORY) + 1
        new_entry = {
            "transaction": {
                "id": new_id,
                "amount": amount,
                "merchant": merchant
            },
            "prediction": {
                "is_fraud": bool(prediction_class),
                "risk_score": risk_score
            }
        }
        SIMULATED_HISTORY.insert(0, new_entry) # Taaki naya transaction sabse upar dikhe

        return jsonify({
            "success": True, 
            "prediction": {
                "is_fraud": bool(prediction_class),
                "risk_score": risk_score
            }
        })

    except Exception as e:
        print(f"PREDICT ERROR: {str(e)}")
        return jsonify({"success": False, "error": str(e)})


@app.route("/api/history")
@app.route("/history")
def get_history():
    try:
        # Bina database ke direct memory array return karega
        return jsonify({"success": True, "history": SIMULATED_HISTORY})
    except Exception as e:
        print(f"API ERROR: {str(e)}") 
        return jsonify({"success": False, "error": str(e)})


# --- MOCK DB DEBUG ROUTES (FRONT-END KO CRASH SE BACHANE KE LIYE) ---

@app.route("/env-test")
def env_test():
    return {
        "MYSQLHOST": "Simulation Mode (No DB Required)",
        "MYSQLUSER": "Mock User",
        "MYSQLDATABASE": "Mock DB",
        "MYSQLPORT": "3306"
    }

@app.route("/db-check")
def db_check():
    return {
        "host": "localhost_simulated",
        "database": "credit_card_sim",
        "user": "root_sim",
        "password_exists": True,
        "port": "3306"
    }

@app.route("/mysql-url")
def mysql_url():
    return {"mysql_url_exists": True}

@app.route("/db-test")
def db_test():
    return {"success": True, "result": 1}

@app.route("/connection-info")
def connection_info():
    return {
        "host": "Simulation Mode",
        "user": "Mock User",
        "database": "Mock DB",
        "port": "3306",
        "mysql_url_exists": True
    }

@app.route("/mysql-url-test")
def mysql_url_test():
    return {
        "success": True,
        "current_user": "Simulation_User"
    }

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
