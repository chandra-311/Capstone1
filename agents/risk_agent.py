import httpx
import json
from utils.logger import setup_logger
from config.settings import MCP_RISK_RULES_URL

logger = setup_logger("RiskAgent")

async def analyze_financial_risk(
    credit_score: int,
    income: float,
    existing_liabilities: float,
    loan_amount: float,
    loan_tenure_months: int
) -> dict:
    """Query RiskRulesDB and analyze financial risk."""
    logger.info(f"Analyzing financial risk for loan amount: {loan_amount}")

    try:
        async with httpx.AsyncClient() as client:
            query_data = {
                "credit_score": credit_score,
                "income": income,
                "existing_liabilities": existing_liabilities,
                "loan_amount": loan_amount,
                "loan_tenure_months": loan_tenure_months
            }

            response = await client.post(
                f"{MCP_RISK_RULES_URL}/analyze",
                json=query_data,
                timeout=10.0
            )
            response.raise_for_status()
            result = response.json()

            logger.info(f"Financial risk analysis complete")
            return result

    except Exception as e:
        logger.error(f"Error analyzing financial risk: {str(e)}")
        return {
            "debt_to_income_ratio": 0.5,
            "credit_score_risk_level": "Medium",
            "loan_amount_risk": "Medium",
            "anomaly_detected": False,
            "reasoning": "Unable to perform analysis",
            "risk_score": 0.5
        }

def format_risk_analysis(analysis_result: dict) -> str:
    """Format risk analysis for agent reasoning."""
    return f"""
    Financial Risk Analysis:
    - Debt-to-Income Ratio: {analysis_result['debt_to_income_ratio']:.3f}
    - Credit Score Risk Level: {analysis_result['credit_score_risk_level']}
    - Loan Amount Risk: {analysis_result['loan_amount_risk']}
    - Risk Score: {analysis_result['risk_score']:.2f}
    - Anomalies Detected: {analysis_result['anomaly_detected']}
    - Reasoning: {analysis_result['reasoning']}
    """
