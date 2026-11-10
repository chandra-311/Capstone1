from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class EmploymentType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    SELF_EMPLOYED = "self_employed"
    UNEMPLOYED = "unemployed"

class DecisionStatus(str, Enum):
    APPROVED = "Approved"
    REJECTED = "Rejected"
    REVIEW = "Requires Manual Review"

class LoanApplicationRequest(BaseModel):
    applicant_id: str = Field(..., description="Unique applicant identifier")
    age: int = Field(..., ge=18, le=100, description="Applicant age")
    income: float = Field(..., gt=0, description="Annual income in dollars")
    employment_type: EmploymentType = Field(..., description="Employment type")
    credit_score: int = Field(..., ge=300, le=850, description="Credit score")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount")
    loan_tenure_months: int = Field(..., gt=0, le=360, description="Loan tenure in months")
    existing_liabilities: float = Field(default=0, ge=0, description="Total existing liabilities")
    location: str = Field(..., description="Applicant location/state")
    application_timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

class ApplicantProfileOutput(BaseModel):
    income_stability_score: float = Field(description="0-1 score for income stability")
    employment_risk: str = Field(description="Low/Medium/High employment risk")
    credit_history_summary: str = Field(description="Summary of credit history")
    completeness_flags: list[str] = Field(default_factory=list, description="Completeness issues")

class FinancialRiskOutput(BaseModel):
    debt_to_income_ratio: float = Field(description="DTI ratio calculation")
    credit_score_risk_level: str = Field(description="Low/Medium/High risk based on credit score")
    loan_amount_risk: str = Field(description="Risk assessment of loan amount")
    anomaly_detected: bool = Field(description="Whether anomalies were detected")
    reasoning: str = Field(description="Reasoning for risk assessment")

class LoanDecisionOutput(BaseModel):
    decision: DecisionStatus = Field(description="Final decision")
    risk_score: float = Field(ge=0, le=1, description="Overall risk score")
    confidence_level: float = Field(ge=0, le=1, description="Decision confidence")
    key_factors: list[str] = Field(description="Key decision factors")
    explanation: str = Field(description="Detailed explanation of decision")

class ComplianceActionOutput(BaseModel):
    action_taken: str = Field(description="Action taken")
    notification_sent: bool = Field(description="Whether notification was sent")
    case_id: str = Field(description="Case ID for tracking")
    timestamp: datetime = Field(description="Action timestamp")
    summary: str = Field(description="Action summary")

class LoanApplicationResponse(BaseModel):
    applicant_id: str
    decision: DecisionStatus
    risk_score: float
    confidence_level: float
    explanation: str
    key_factors: list[str]
    case_id: str
    timestamp: datetime
    detailed_analysis: dict = Field(default_factory=dict)
