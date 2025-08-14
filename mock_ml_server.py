#!/usr/bin/env python3
"""
Mock ML server for testing the MCP server without needing the actual FastAPI ML service.
This simulates the employee churn prediction API.
"""

from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    """Mock prediction endpoint that returns fake but realistic predictions."""
    try:
        data = request.get_json()
        
        # Extract features for mock logic
        satisfaction = data.get('EmployeeSatisfaction', 0.5)
        years = data.get('YearsAtCompany', 5)
        position = data.get('Position', 'Non-Manager')
        salary = data.get('Salary', 5.0)
        
        # Simple mock logic: low satisfaction or very low salary = higher churn risk
        churn_probability = 0.1  # base probability
        
        if satisfaction < 0.3:
            churn_probability += 0.6
        elif satisfaction < 0.6:
            churn_probability += 0.2
            
        if salary < 3.0:
            churn_probability += 0.3
            
        if years < 2:
            churn_probability += 0.2
        elif years > 10:
            churn_probability += 0.1
            
        # Add some randomness
        churn_probability += random.uniform(-0.1, 0.1)
        churn_probability = max(0.0, min(1.0, churn_probability))
        
        prediction = 1 if churn_probability > 0.5 else 0
        
        return jsonify({
            "prediction": prediction,
            "churn_probability": round(churn_probability, 3),
            "risk_level": "High" if churn_probability > 0.7 else "Medium" if churn_probability > 0.3 else "Low",
            "input_data": data
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "Mock ML Server"})

if __name__ == '__main__':
    print("🤖 Starting Mock ML Server on http://127.0.0.1:8000")
    print("📊 Endpoint: POST /predict")
    print("💚 Health check: GET /health")
    app.run(host='127.0.0.1', port=8000, debug=True)