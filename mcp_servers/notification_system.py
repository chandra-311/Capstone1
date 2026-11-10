from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

app = FastAPI(title="NotificationSystem MCP Server")

# In-memory storage for demo purposes
case_registry = {}

class NotificationRequest(BaseModel):
    applicant_id: str
    decision: str
    risk_score: float
    confidence_level: float
    explanation: str
    key_factors: list[str]

class NotificationResponse(BaseModel):
    action_taken: str
    notification_sent: bool
    case_id: str
    timestamp: datetime
    summary: str

def generate_case_id() -> str:
    return f"CASE-{uuid.uuid4().hex[:8].upper()}"

@app.post("/notify", response_model=NotificationResponse)
async def send_notification(request: NotificationRequest):
    try:
        case_id = generate_case_id()
        timestamp = datetime.utcnow()

        # Store case record
        case_registry[case_id] = {
            "applicant_id": request.applicant_id,
            "decision": request.decision,
            "risk_score": request.risk_score,
            "confidence_level": request.confidence_level,
            "timestamp": timestamp,
            "status": "notified"
        }

        # Determine action
        if request.decision == "Approved":
            action = "Sent approval notification and initiated loan processing"
        elif request.decision == "Rejected":
            action = "Sent rejection notification with appeal information"
        else:  # Requires Manual Review
            action = "Escalated to manual review team"

        summary = f"Decision: {request.decision}, Risk: {request.risk_score:.2f}, Confidence: {request.confidence_level:.2f}"

        return NotificationResponse(
            action_taken=action,
            notification_sent=True,
            case_id=case_id,
            timestamp=timestamp,
            summary=summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/case/{case_id}")
async def get_case(case_id: str):
    if case_id not in case_registry:
        raise HTTPException(status_code=404, detail="Case not found")
    return case_registry[case_id]

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "NotificationSystem", "cases_processed": len(case_registry)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
