# Real-Time Risk & Fraud Analytics Pipeline

An enterprise-grade analytical infrastructure designed to detect, track, and prevent multi-million dollar transactional fraud vectors. This pipeline integrates real-time API screening workflows with deep analytical queries executed via Snowflake SQL frameworks.

## 🌟 Key Business Value Delivered
- **Velocity Tracking Engine:** Identifies account takeovers by auditing geographic variations inside small action windows.
- **Data Validation Integrity:** Uses programmatic frameworks to isolate corrupted payloads before ingestion.
- **Operational Scalability:** Designed to optimize manual review queues by routing transaction threats based on tier scoring models.

## 🖥️ Local API Execution & Verification
To verify the real-time data validation logic, the FastAPI server was initialized locally using `uvicorn app.main:app --reload`. 

### Mock Transaction Ingestion Test:
Using an API client, a sample high-risk payload was sent to the endpoint `http://127.0.0`:

```json
// Inbound API Payload Sent
{
  "transaction_id": "TXN1005",
  "user_id": "USR901",
  "merchant_id": "MERCH02",
  "amount": 12000.00,
  "device_id": "DEV_IPHONE_X",
  "ip_address": "198.51.100.42",
  "location": "Kolkata",
  "timestamp": "2026-07-13T10:04:10Z"
}
```

### Risk Engine Terminal Response Output:
```json
// Automated JSON Verification Status Return
{
  "status": "success",
  "assessment": {
    "transaction_id": "TXN1005",
    "risk_score": 40,
    "decision": "MANUAL_REVIEW",
    "triggered_flags": ["HIGH_TICKET_ALERT"],
    "processed_at": "2026-07-13T10:04:15.124Z"
  }
}
```
This output confirms that the Pydantic data contract validated the data structure perfectly, and the routing logic automatically sent the transaction to the risk team's manual review queue.
