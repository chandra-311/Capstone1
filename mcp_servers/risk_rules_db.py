from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="RiskRulesDB MCP Server")

class RiskAnalysisQuery(BaseModel):
    credit_score: int
    income: float
    existing_liabilities: float
    loan_amount: float
    loan_tenure_months: int

class RiskAnalysisResponse(BaseModel):
    debt_to_income_ratio: float
    credit_score_risk_level: str
    loan_amount_risk: str
    anomaly_detected: bool
    reasoning: str
    risk_score: float

def calculate_dti_ratio(income: float, existing_liabilities: float, loan_amount: float, tenure_months: int) -> tuple[float, str]:
    monthly_income = income / 12
    monthly_loan_payment = loan_amount / tenure_months
    total_monthly_debt = existing_liabilities + monthly_loan_payment

    dti_ratio = total_monthly_debt / monthly_income if monthly_income > 0 else 0.0
    dti_ratio = min(dti_ratio, 2.0)  # Cap at 2.0 for extreme cases

    return dti_ratio, monthly_income, monthly_loan_payment

def assess_credit_risk(credit_score: int) -> str:
    if credit_score >= 750:
        return "Low"
    elif credit_score >= 700:
        return "Low-Medium"
    elif credit_score >= 650:
        return "Medium"
    elif credit_score >= 600:
        return "Medium-High"
    else:
        return "High"

def assess_loan_amount_risk(loan_amount: float, income: float) -> str:
    loan_to_income = loan_amount / income if income > 0 else 0

    if loan_to_income < 2:
        return "Low"
    elif loan_to_income < 4:
        return "Medium"
    elif loan_to_income < 6:
        return "Medium-High"
    else:
        return "High"

def detect_anomalies(credit_score: int, dti_ratio: float, loan_amount: float, income: float) -> tuple[bool, list[str]]:
    anomalies = []

    if credit_score < 500 and loan_amount > income * 3:
        anomalies.append("Low credit score with high loan amount")

    if dti_ratio > 1.0:
        anomalies.append("Debt-to-income ratio exceeds 100%")

    if loan_amount > income * 5:
        anomalies.append("Loan amount significantly exceeds annual income")

    return len(anomalies) > 0, anomalies

@app.post("/analyze", response_model=RiskAnalysisResponse)
async def analyze_risk(query: RiskAnalysisQuery):
    try:
        dti_ratio, monthly_income, monthly_payment = calculate_dti_ratio(
            query.income, query.existing_liabilities, query.loan_amount, query.loan_tenure_months
        )

        credit_risk = assess_credit_risk(query.credit_score)
        loan_risk = assess_loan_amount_risk(query.loan_amount, query.income)
        anomaly_detected, anomalies = detect_anomalies(
            query.credit_score, dti_ratio, query.loan_amount, query.income
        )

        # Calculate composite risk score
        credit_risk_weight = 0.3
        dti_risk_weight = 0.3
        loan_amount_risk_weight = 0.2
        anomaly_weight = 0.2

        credit_risk_score = {"Low": 0.1, "Low-Medium": 0.25, "Medium": 0.5, "Medium-High": 0.75, "High": 0.95}.get(credit_risk, 0.5)
        dti_risk_score = min(dti_ratio / 0.5, 1.0)  # 0.5 is considered high DTI
        loan_amount_risk_score = {"Low": 0.1, "Medium": 0.4, "Medium-High": 0.7, "High": 0.95}.get(loan_risk, 0.5)
        anomaly_score = 0.8 if anomaly_detected else 0.0

        composite_risk_score = (
            credit_risk_weight * credit_risk_score +
            dti_risk_weight * dti_risk_score +
            loan_amount_risk_weight * loan_amount_risk_score +
            anomaly_weight * anomaly_score
        )

        reasoning = f"DTI: {dti_ratio:.2f} ({credit_risk} credit), Loan-to-Income: {query.loan_amount/query.income:.2f}x"
        if anomalies:
            reasoning += f". Anomalies: {', '.join(anomalies)}"

        return RiskAnalysisResponse(
            debt_to_income_ratio=dti_ratio,
            credit_score_risk_level=credit_risk,
            loan_amount_risk=loan_risk,
            anomaly_detected=anomaly_detected,
            reasoning=reasoning,
            risk_score=min(composite_risk_score, 1.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RiskRulesDB"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
