from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from datetime import datetime
from models.loan_application import LoanApplicationRequest, LoanApplicationResponse
from orchestrator.langgraph_engine import execute_workflow
from utils.logger import setup_logger

logger = setup_logger("Microservice")

app = FastAPI(
    title="Loan Approval Microservice",
    description="Multi-Agent Agentic AI Loan Application System",
    version="1.0.0"
)

# Add CORS middleware for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
application_store = {}

@app.post("/api/apply", response_model=LoanApplicationResponse)
async def submit_loan_application(application: LoanApplicationRequest):
    """Submit a loan application for evaluation."""
    logger.info(f"Received loan application from {application.applicant_id}")

    try:
        # Execute the orchestration workflow
        response = await execute_workflow(application)

        # Store application result
        application_store[application.applicant_id] = {
            "application": application.model_dump(),
            "response": response.model_dump(),
            "submitted_at": datetime.utcnow().isoformat()
        }

        logger.info(f"Application processed successfully: {application.applicant_id}")
        return response

    except Exception as e:
        logger.error(f"Error processing application: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status/{applicant_id}")
async def get_application_status(applicant_id: str):
    """Get the status of a loan application."""
    if applicant_id not in application_store:
        raise HTTPException(status_code=404, detail="Application not found")

    return application_store[applicant_id]

@app.get("/api/applications")
async def list_applications():
    """List all processed applications."""
    return {
        "total": len(application_store),
        "applications": list(application_store.keys())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Loan Approval Microservice",
        "applications_processed": len(application_store)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
