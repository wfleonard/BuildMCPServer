#!/usr/bin/env python3
"""
Mock FastAPI ML service for testing the MCP server.
This creates a simple endpoint that returns mock churn predictions.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="Mock Churn Prediction Service")

class EmployeeData(BaseModel):
    YearsAtCompany: float
    EmployeeSatisfaction: float
    Position: str
    Salary: float

@app.post("/predict")
async def predict_churn(employee: EmployeeData):
    """
    Mock prediction endpoint that returns fake churn predictions
    based on simple rules for testing purposes.
    """
    # Simple mock logic: higher satisfaction = lower churn probability
    satisfaction_factor = employee.EmployeeSatisfaction
    years_factor = min(employee.YearsAtCompany / 10, 1.0)  # Cap at 10 years
    salary_factor = min(employee.Salary / 100000, 1.0)  # Normalize salary
    
    # Calculate mock churn probability (0-1)
    churn_probability = max(0, 1 - (satisfaction_factor * 0.7 + years_factor * 0.2 + salary_factor * 0.1))
    
    # Add some randomness
    churn_probability += random.uniform(-0.1, 0.1)
    churn_probability = max(0, min(1, churn_probability))
    
    will_churn = churn_probability > 0.5
    
    return {
        "prediction": "churn" if will_churn else "stay",
        "churn_probability": round(churn_probability, 3),
        "confidence": random.uniform(0.7, 0.95),
        "employee_data": employee.dict()
    }

@app.get("/")
async def root():
    return {"message": "Mock Churn Prediction Service", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)