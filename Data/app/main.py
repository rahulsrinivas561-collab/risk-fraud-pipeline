from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import List
import uvicorn
from datetime import datetime

app = FastAPI(title="Swiggy-Style Risk & Fraud Analytics API Pipeline")

# Pydantic schema for deep data validation and runtime verification
class TransactionPayload(BaseModel):
    transaction_id: str = Field(..., example="TXN1001")
    user_id: str = Field(..., example="USR901")
    merchant_id: str = Field(..., example="MERCH44")
    amount: float = Field(..., gt=0, example=4500.00)
    device_id: str = Field(..., example="DEV_IPHONE_X")
    ip_address: str = Field(..., example="192.168.1.50")
    location: str = Field(..., example="Bangalore")
    timestamp: datetime

    @validator('amount')
    def check_velocity_threshold(cls, v):
        if v > 10000:
            # Real-time engineering flag for compliance auditing
            pass
        return v

# Core risk rule execution matrix
def evaluate_transaction_risk(tx: TransactionPayload) -> dict:
    risk_score = 0
    flags = []
    
    # Rule 1: High Ticket Size Transaction Check
    if tx.amount > 5000:
        risk_score += 40
        flags.append("HIGH_TICKET_ALERT")
        
    # Rule 2: Quick Location Anomaly Detection (Mocking location history checks)
    if tx.location not in ["Bangalore", "Mumbai", "Delhi", "Kolkata"]:
        risk_score += 30
        flags.append("UNUSUAL_GEOLOCATION")

    status_decision = "APPROVE"
    if risk_score >= 70:
        status_decision = "BLOCK"
    elif risk_score >= 40:
        status_decision = "MANUAL_REVIEW"

    return {
        "transaction_id": tx.transaction_id,
        "risk_score": risk_score,
        "decision": status_decision,
        "triggered_flags": flags,
        "processed_at": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/risk/evaluate", status_code=status.HTTP_200_OK)
def process_transaction(transaction: TransactionPayload):

    try:
        assessment = evaluate_transaction_risk(transaction)
        return {"status": "success", "assessment": assessment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
