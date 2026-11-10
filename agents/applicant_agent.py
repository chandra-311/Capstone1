import httpx
import json
from utils.logger import setup_logger
from config.settings import MCP_APPLICANT_DB_URL

logger = setup_logger("ApplicantAgent")

async def analyze_applicant_profile(
    applicant_id: str,
    age: int,
    income: float,
    employment_type: str,
    location: str
) -> dict:
    """Query ApplicantDB and analyze applicant profile."""
    logger.info(f"Analyzing applicant profile for {applicant_id}")

    try:
        async with httpx.AsyncClient() as client:
            query_data = {
                "applicant_id": applicant_id,
                "age": age,
                "income": income,
                "employment_type": employment_type,
                "location": location
            }

            response = await client.post(
                f"{MCP_APPLICANT_DB_URL}/query",
                json=query_data,
                timeout=10.0
            )
            response.raise_for_status()
            result = response.json()

            logger.info(f"Applicant profile analysis complete: {applicant_id}")
            return result

    except Exception as e:
        logger.error(f"Error analyzing applicant profile: {str(e)}")
        return {
            "income_stability_score": 0.5,
            "employment_risk": "Medium",
            "credit_history_summary": "Unable to retrieve",
            "completeness_flags": ["Data retrieval error"]
        }

def format_applicant_analysis(analysis_result: dict) -> str:
    """Format applicant analysis for agent reasoning."""
    return f"""
    Applicant Profile Analysis:
    - Income Stability Score: {analysis_result['income_stability_score']:.2f}/1.0
    - Employment Risk: {analysis_result['employment_risk']}
    - Credit History: {analysis_result['credit_history_summary']}
    - Completeness Flags: {', '.join(analysis_result['completeness_flags']) if analysis_result['completeness_flags'] else 'None'}
    """
