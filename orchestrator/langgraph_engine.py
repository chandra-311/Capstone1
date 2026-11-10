import asyncio
import json
from datetime import datetime
from typing import TypedDict, Any
from utils.logger import setup_logger
from agents import applicant_agent, risk_agent, decision_agent, compliance_agent
from models.loan_application import (
    LoanApplicationRequest, LoanApplicationResponse, DecisionStatus
)

logger = setup_logger("LangGraphOrchestrator")

class WorkflowState(TypedDict):
    """State management for the loan approval workflow."""
    application: dict
    applicant_analysis: dict
    risk_analysis: dict
    decision_synthesis: dict
    compliance_action: dict
    error_occurred: bool
    error_message: str

async def node_analyze_applicant(state: WorkflowState) -> WorkflowState:
    """Node 1: Analyze applicant profile."""
    logger.info("Entering node_analyze_applicant")

    try:
        app = state["application"]
        analysis = await applicant_agent.analyze_applicant_profile(
            applicant_id=app["applicant_id"],
            age=app["age"],
            income=app["income"],
            employment_type=app["employment_type"],
            location=app["location"]
        )
        state["applicant_analysis"] = analysis
        logger.info(f"Applicant analysis complete")
    except Exception as e:
        logger.error(f"Error in applicant analysis: {str(e)}")
        state["error_occurred"] = True
        state["error_message"] = str(e)

    return state

async def node_analyze_risk(state: WorkflowState) -> WorkflowState:
    """Node 2: Analyze financial risk."""
    logger.info("Entering node_analyze_risk")

    if state.get("error_occurred"):
        return state

    try:
        app = state["application"]
        analysis = await risk_agent.analyze_financial_risk(
            credit_score=app["credit_score"],
            income=app["income"],
            existing_liabilities=app["existing_liabilities"],
            loan_amount=app["loan_amount"],
            loan_tenure_months=app["loan_tenure_months"]
        )
        state["risk_analysis"] = analysis
        logger.info(f"Risk analysis complete")
    except Exception as e:
        logger.error(f"Error in risk analysis: {str(e)}")
        state["error_occurred"] = True
        state["error_message"] = str(e)

    return state

async def node_synthesize_decision(state: WorkflowState) -> WorkflowState:
    """Node 3: Synthesize decision from all factors."""
    logger.info("Entering node_synthesize_decision")

    if state.get("error_occurred"):
        return state

    try:
        app = state["application"]
        applicant_analysis = state["applicant_analysis"]
        risk_analysis = state["risk_analysis"]

        # Calculate applicant profile risk (inverse of stability)
        applicant_profile_risk = 1.0 - applicant_analysis["income_stability_score"]

        decision = await decision_agent.synthesize_decision(
            applicant_profile_risk=applicant_profile_risk,
            financial_risk_score=risk_analysis["risk_score"],
            credit_score=app["credit_score"],
            dti_ratio=risk_analysis["debt_to_income_ratio"],
            employment_risk=applicant_analysis["employment_risk"],
            anomaly_detected=risk_analysis["anomaly_detected"]
        )
        state["decision_synthesis"] = decision
        logger.info(f"Decision synthesized: {decision['recommendation']}")
    except Exception as e:
        logger.error(f"Error in decision synthesis: {str(e)}")
        state["error_occurred"] = True
        state["error_message"] = str(e)

    return state

async def node_compliance_and_notification(state: WorkflowState) -> WorkflowState:
    """Node 4: Handle compliance and send notifications."""
    logger.info("Entering node_compliance_and_notification")

    if state.get("error_occurred"):
        decision_synthesis = {
            "final_risk_score": 0.8,
            "recommendation": "Requires Manual Review",
            "confidence_level": 0.3,
            "key_factors": ["System error occurred"],
            "decision_reasoning": state.get("error_message", "Unknown error")
        }
    else:
        decision_synthesis = state["decision_synthesis"]

    # Map recommendation to decision status
    recommendation_map = {
        "Approve": DecisionStatus.APPROVED,
        "Reject": DecisionStatus.REJECTED,
        "Requires Manual Review": DecisionStatus.REVIEW
    }
    decision_status = recommendation_map.get(
        decision_synthesis["recommendation"],
        DecisionStatus.REVIEW
    )

    try:
        action = await compliance_agent.send_notification_and_log(
            applicant_id=state["application"]["applicant_id"],
            decision=decision_status.value,
            risk_score=decision_synthesis["final_risk_score"],
            confidence_level=decision_synthesis["confidence_level"],
            explanation=decision_synthesis["decision_reasoning"],
            key_factors=decision_synthesis["key_factors"]
        )
        state["compliance_action"] = action
        logger.info(f"Compliance action complete. Case: {action['case_id']}")
    except Exception as e:
        logger.error(f"Error in compliance processing: {str(e)}")
        state["compliance_action"] = {
            "action_taken": "Error processing",
            "notification_sent": False,
            "case_id": f"CASE-ERROR-{int(datetime.utcnow().timestamp())}",
            "timestamp": datetime.utcnow().isoformat(),
            "summary": str(e)
        }

    return state

async def execute_workflow(application: LoanApplicationRequest) -> LoanApplicationResponse:
    """Execute the complete loan approval workflow."""
    logger.info(f"Starting workflow for applicant: {application.applicant_id}")

    # Initialize state
    state: WorkflowState = {
        "application": application.model_dump(),
        "applicant_analysis": {},
        "risk_analysis": {},
        "decision_synthesis": {},
        "compliance_action": {},
        "error_occurred": False,
        "error_message": ""
    }

    # Execute nodes sequentially (can be parallelized for applicable nodes)
    state = await node_analyze_applicant(state)
    state = await node_analyze_risk(state)
    state = await node_synthesize_decision(state)
    state = await node_compliance_and_notification(state)

    # Build response
    decision_synthesis = state["decision_synthesis"] if state["decision_synthesis"] else {
        "final_risk_score": 0.5,
        "recommendation": "Requires Manual Review",
        "confidence_level": 0.5,
        "key_factors": [],
        "decision_reasoning": "Unable to complete analysis"
    }

    recommendation_map = {
        "Approve": DecisionStatus.APPROVED,
        "Reject": DecisionStatus.REJECTED,
        "Requires Manual Review": DecisionStatus.REVIEW
    }

    decision_status = recommendation_map.get(
        decision_synthesis["recommendation"],
        DecisionStatus.REVIEW
    )

    compliance = state["compliance_action"]

    response = LoanApplicationResponse(
        applicant_id=application.applicant_id,
        decision=decision_status,
        risk_score=decision_synthesis["final_risk_score"],
        confidence_level=decision_synthesis["confidence_level"],
        explanation=decision_synthesis["decision_reasoning"],
        key_factors=decision_synthesis["key_factors"],
        case_id=compliance.get("case_id", "CASE-UNKNOWN"),
        timestamp=datetime.utcnow(),
        detailed_analysis={
            "applicant_analysis": state["applicant_analysis"],
            "risk_analysis": state["risk_analysis"],
            "decision_synthesis": decision_synthesis
        }
    )

    logger.info(f"Workflow complete for {application.applicant_id}: {decision_status.value}")
    return response
