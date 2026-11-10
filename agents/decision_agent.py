import httpx
import json
from utils.logger import setup_logger
from config.settings import MCP_DECISION_SYNTHESIS_URL

logger = setup_logger("DecisionAgent")

async def synthesize_decision(
    applicant_profile_risk: float,
    financial_risk_score: float,
    credit_score: int,
    dti_ratio: float,
    employment_risk: str,
    anomaly_detected: bool
) -> dict:
    """Query DecisionSynthesis and make loan decision."""
    logger.info("Synthesizing loan decision")

    try:
        async with httpx.AsyncClient() as client:
            query_data = {
                "applicant_profile_risk": applicant_profile_risk,
                "financial_risk_score": financial_risk_score,
                "credit_score": credit_score,
                "dti_ratio": dti_ratio,
                "employment_risk": employment_risk,
                "anomaly_detected": anomaly_detected
            }

            response = await client.post(
                f"{MCP_DECISION_SYNTHESIS_URL}/synthesize",
                json=query_data,
                timeout=10.0
            )
            response.raise_for_status()
            result = response.json()

            logger.info(f"Decision synthesized: {result['recommendation']}")
            return result

    except Exception as e:
        logger.error(f"Error synthesizing decision: {str(e)}")
        return {
            "final_risk_score": 0.5,
            "recommendation": "Requires Manual Review",
            "confidence_level": 0.5,
            "key_factors": ["System error - manual review required"],
            "decision_reasoning": "Unable to perform decision synthesis"
        }

def format_decision_synthesis(synthesis_result: dict) -> str:
    """Format decision synthesis for agent reasoning."""
    return f"""
    Decision Synthesis:
    - Final Risk Score: {synthesis_result['final_risk_score']:.2f}
    - Recommendation: {synthesis_result['recommendation']}
    - Confidence Level: {synthesis_result['confidence_level']:.2f}
    - Key Factors: {', '.join(synthesis_result['key_factors'])}
    - Reasoning: {synthesis_result['decision_reasoning']}
    """
