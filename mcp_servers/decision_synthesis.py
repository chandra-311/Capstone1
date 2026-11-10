from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="DecisionSynthesis MCP Server")

class SynthesisQuery(BaseModel):
    applicant_profile_risk: float
    financial_risk_score: float
    credit_score: int
    dti_ratio: float
    employment_risk: str
    anomaly_detected: bool

class DecisionSynthesisResponse(BaseModel):
    final_risk_score: float
    recommendation: str
    confidence_level: float
    key_factors: list[str]
    decision_reasoning: str

def synthesize_decision(
    applicant_profile_risk: float,
    financial_risk_score: float,
    credit_score: int,
    dti_ratio: float,
    employment_risk: str,
    anomaly_detected: bool
) -> tuple[float, str, float, list[str]]:
    """Synthesize all risk factors into a final decision."""

    # Weight the different risk factors
    weights = {
        "applicant_profile": 0.25,
        "financial_risk": 0.35,
        "credit_quality": 0.20,
        "employment_stability": 0.20
    }

    # Normalize credit score to 0-1 range (lower is better risk)
    credit_risk = (850 - credit_score) / 550

    # Employment risk mapping
    employment_risk_scores = {
        "Low": 0.1,
        "Medium-Low": 0.25,
        "Medium": 0.5,
        "High": 0.8
    }
    employment_score = employment_risk_scores.get(employment_risk, 0.5)

    # Composite risk score
    composite_risk = (
        weights["applicant_profile"] * applicant_profile_risk +
        weights["financial_risk"] * financial_risk_score +
        weights["credit_quality"] * credit_risk +
        weights["employment_stability"] * employment_score
    )

    # Adjust for anomalies
    if anomaly_detected:
        composite_risk += 0.15
        composite_risk = min(composite_risk, 1.0)

    # Calculate confidence
    base_confidence = 0.85
    if anomaly_detected:
        base_confidence -= 0.1
    if dti_ratio > 0.5:
        base_confidence -= 0.05
    confidence = max(base_confidence, 0.5)

    # Recommendation logic
    if composite_risk < 0.3:
        recommendation = "Approve"
    elif composite_risk < 0.6:
        recommendation = "Requires Manual Review"
    else:
        recommendation = "Reject"

    # Key factors
    factors = []
    if credit_score > 750:
        factors.append("Excellent credit score")
    elif credit_score < 600:
        factors.append("Low credit score")

    if dti_ratio < 0.3:
        factors.append("Healthy debt-to-income ratio")
    elif dti_ratio > 0.5:
        factors.append("High debt-to-income ratio")

    if employment_risk == "Low":
        factors.append("Stable employment")
    elif employment_risk == "High":
        factors.append("Employment instability concern")

    if anomaly_detected:
        factors.append("Anomalies detected in application")

    return composite_risk, recommendation, confidence, factors

@app.post("/synthesize", response_model=DecisionSynthesisResponse)
async def synthesize(query: SynthesisQuery):
    try:
        risk_score, recommendation, confidence, factors = synthesize_decision(
            query.applicant_profile_risk,
            query.financial_risk_score,
            query.credit_score,
            query.dti_ratio,
            query.employment_risk,
            query.anomaly_detected
        )

        reasoning = f"Based on comprehensive risk assessment: applicant profile risk ({query.applicant_profile_risk:.2f}), "
        reasoning += f"financial risk ({query.financial_risk_score:.2f}), employment risk ({query.employment_risk}). "
        if query.anomaly_detected:
            reasoning += "Anomalies detected. "
        reasoning += f"Composite risk score: {risk_score:.2f}"

        return DecisionSynthesisResponse(
            final_risk_score=risk_score,
            recommendation=recommendation,
            confidence_level=confidence,
            key_factors=factors,
            decision_reasoning=reasoning
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "DecisionSynthesis"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
