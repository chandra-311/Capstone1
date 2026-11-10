from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

app = FastAPI(title="ApplicantDB MCP Server")

class ApplicantQuery(BaseModel):
    applicant_id: str
    age: int
    income: float
    employment_type: str
    location: str

class IncomeStability(BaseModel):
    score: float
    factors: list[str]

class CreditHistorySummary(BaseModel):
    years_of_history: int
    summary: str
    flags: list[str]

class ApplicantDBResponse(BaseModel):
    income_stability_score: float
    income_details: IncomeStability
    employment_risk: str
    credit_history_summary: str
    completeness_flags: list[str]

def analyze_income_stability(age: int, income: float, employment_type: str) -> IncomeStability:
    score = 0.5
    factors = []

    if employment_type == "full_time":
        score += 0.2
        factors.append("Full-time employment")
    elif employment_type == "part_time":
        score -= 0.1
        factors.append("Part-time employment")
    elif employment_type == "self_employed":
        score -= 0.05
        factors.append("Self-employed with variable income")

    if 25 <= age <= 55:
        score += 0.1
        factors.append("Prime working age")
    elif age > 55:
        score -= 0.1
        factors.append("Near retirement age")

    if income > 100000:
        score += 0.2
        factors.append("High income level")
    elif income > 50000:
        score += 0.1
        factors.append("Moderate income level")

    score = min(1.0, max(0.0, score))
    return IncomeStability(score=score, factors=factors)

def analyze_employment_risk(employment_type: str, age: int) -> str:
    if employment_type == "unemployed":
        return "High"
    elif employment_type == "self_employed":
        return "Medium"
    elif employment_type == "part_time":
        return "Medium-Low"
    else:  # full_time
        return "Low"

def get_credit_history(applicant_id: str) -> CreditHistorySummary:
    hash_val = hash(applicant_id)
    years = (abs(hash_val) % 20) + 1

    if years >= 10:
        summary = "Excellent credit history with consistent positive record"
        flags = []
    elif years >= 5:
        summary = "Good credit history with some minor issues"
        flags = ["Minor late payments in history"] if abs(hash_val) % 3 == 0 else []
    else:
        summary = "Limited credit history, recent establishment"
        flags = ["Short credit history"]

    return CreditHistorySummary(years_of_history=years, summary=summary, flags=flags)

@app.post("/query", response_model=ApplicantDBResponse)
async def query_applicant_db(query: ApplicantQuery):
    try:
        income_stability = analyze_income_stability(query.age, query.income, query.employment_type)
        employment_risk = analyze_employment_risk(query.employment_type, query.age)
        credit_history = get_credit_history(query.applicant_id)

        return ApplicantDBResponse(
            income_stability_score=income_stability.score,
            income_details=income_stability,
            employment_risk=employment_risk,
            credit_history_summary=credit_history.summary,
            completeness_flags=credit_history.flags
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ApplicantDB"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
