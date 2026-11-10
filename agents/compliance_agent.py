import httpx
import json
from datetime import datetime
from utils.logger import setup_logger
from config.settings import MCP_NOTIFICATION_URL

logger = setup_logger("ComplianceAgent")

async def send_notification_and_log(
    applicant_id: str,
    decision: str,
    risk_score: float,
    confidence_level: float,
    explanation: str,
    key_factors: list
) -> dict:
    """Send notification through NotificationSystem."""
    logger.info(f"Processing compliance and notification for {applicant_id}")

    try:
        async with httpx.AsyncClient() as client:
            notification_data = {
                "applicant_id": applicant_id,
                "decision": decision,
                "risk_score": risk_score,
                "confidence_level": confidence_level,
                "explanation": explanation,
                "key_factors": key_factors
            }

            response = await client.post(
                f"{MCP_NOTIFICATION_URL}/notify",
                json=notification_data,
                timeout=10.0
            )
            response.raise_for_status()
            result = response.json()

            logger.info(f"Compliance action completed. Case ID: {result['case_id']}")
            return result

    except Exception as e:
        logger.error(f"Error in compliance processing: {str(e)}")
        return {
            "action_taken": "Error in notification system",
            "notification_sent": False,
            "case_id": "CASE-ERROR",
            "timestamp": datetime.utcnow().isoformat(),
            "summary": "Unable to process notification"
        }

def format_compliance_action(action_result: dict) -> str:
    """Format compliance action for audit trail."""
    return f"""
    Compliance & Action Orchestration:
    - Action Taken: {action_result['action_taken']}
    - Notification Sent: {action_result['notification_sent']}
    - Case ID: {action_result['case_id']}
    - Timestamp: {action_result['timestamp']}
    - Summary: {action_result['summary']}
    """
