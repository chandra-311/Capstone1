import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL_NAME = "claude-opus-5-5-20250805"

# Service Configuration
FASTAPI_HOST = "0.0.0.0"
FASTAPI_PORT = 8000

STREAMLIT_PORT = 8501

# MCP Server Configuration
MCP_APPLICANT_DB_URL = "http://localhost:8001"
MCP_RISK_RULES_URL = "http://localhost:8002"
MCP_DECISION_SYNTHESIS_URL = "http://localhost:8003"
MCP_NOTIFICATION_URL = "http://localhost:8004"

# Application Constants
APPROVED_THRESHOLD = 0.7
REVIEW_THRESHOLD = 0.4
CONFIDENCE_THRESHOLD = 0.6

# Loan Amount Limits
MIN_LOAN_AMOUNT = 50000
MAX_LOAN_AMOUNT = 5000000

# Debt-to-Income Ratio
MAX_DTI_RATIO = 0.5

# Credit Score Bands
EXCELLENT_CREDIT = 750
GOOD_CREDIT = 700
FAIR_CREDIT = 650
POOR_CREDIT = 600
