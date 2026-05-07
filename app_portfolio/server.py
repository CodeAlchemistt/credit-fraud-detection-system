from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import os

app = Flask(__name__)
# Enable CORS so your custom HTML/JS frontend can communicate with this API
CORS(app)

# 1. Load the AI Model securely when the server starts
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models', 'fraud_model.pkl'))
try:
    model = joblib.load(model_path)
    print("✅ API Server: Random Forest Model Loaded Successfully")
except FileNotFoundError:
    print("❌ ERROR: Model not found. Make sure 'fraud_model.pkl' exists in the 'models' directory.")
    model = None

# 2. Define the Prediction Endpoint
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded on server'}), 500

    try:
        # Get the JSON data sent from your JavaScript frontend
        data = request.get_json()

        # Extract the user's scenario inputs
        amount = float(data.get('amount', 0))
        time = float(data.get('time', 0))
        v14 = float(data.get('v14', 0))
        v4 = float(data.get('v4', 0))

        # Create the 30-feature array the AI expects
        features = np.zeros(30)
        features[0] = time      
        features[4] = v4         
        features[14] = v14       
        features[29] = amount    

        # Run the AI prediction
        prediction = model.predict([features])
        
        # 0 = Normal, 1 = Fraud
        is_fraud = bool(prediction[0] == 1)

        # Send the result back to the frontend
        return jsonify({
            'success': True,
            'is_fraud': is_fraud,
            'message': 'Fraudulent pattern detected!' if is_fraud else 'Transaction approved.'
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    # Run the server on port 5000
    print("🚀 Starting Flask API server on http://localhost:5000")
    app.run(debug=True, port=5000)