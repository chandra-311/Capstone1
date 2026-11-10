# CREATE - AI-Agent Loan Approval System Setup Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running the Application](#running-the-application)
7. [Health Check](#health-check)
8. [Database Setup](#database-setup)
9. [API Documentation](#api-documentation)
10. [Testing](#testing)
11. [Troubleshooting](#troubleshooting)

---

## Project Overview

**AI-Agent Loan Approval System** is a production-ready multi-agent application that automates loan application analysis using AI agents. It provides explainable decisions (Approved/Rejected/Requires Manual Review) with risk scoring and comprehensive audit trails.

### Key Features
- ✅ Multi-Agent Orchestration (4 specialized AI agents)
- ✅ Real-time Loan Decision Making
- ✅ Explainable AI with Risk Scoring
- ✅ Case Tracking & Compliance Logging
- ✅ RESTful API
- ✅ Interactive Web UI (Streamlit)
- ✅ Health Monitoring

### Technology Stack
- **Frontend**: Streamlit 1.41.1
- **Backend**: FastAPI 0.115.6
- **Orchestration**: LangGraph 0.2.51
- **LLM**: Anthropic Claude Opus 5.5
- **Database**: In-memory (extensible to PostgreSQL, MySQL, MongoDB)
- **Language**: Python 3.9+

---

## System Architecture

### Component Layers

```
┌─────────────────────────────────────────────────────┐
│ PRESENTATION LAYER                                  │
│ Streamlit UI (Port 8501) - Web Interface           │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│ MICROSERVICE LAYER                                  │
│ FastAPI Microservice (Port 8000) - REST API        │
└─────────────────────────┬───────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────┐
│ ORCHESTRATION LAYER                                 │
│ LangGraph Engine - Workflow Coordination            │
└─────────────────────────┬───────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼────┐  ┌────────▼─────┐  ┌───────▼─────┐
│ Applicant  │  │ Financial    │  │ Loan        │
│ Profile    │  │ Risk         │  │ Decision    │
│ Agent      │  │ Agent        │  │ Agent       │
└───────┬────┘  └────────┬─────┘  └───────┬─────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────▼────┐  ┌────────▼─────┐  ┌───────▼─────┐
│ Applicant  │  │ Risk         │  │ Decision    │
│ DB MCP     │  │ Rules MCP    │  │ Synthesis   │
│ (8001)     │  │ (8002)       │  │ MCP (8003)  │
└────────────┘  └──────────────┘  └─────────────┘
```

---

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 18.04+), macOS, Windows (WSL2)
- **Python**: 3.9 or higher
- **RAM**: Minimum 4GB, Recommended 8GB
- **Storage**: 5GB free space

### Required Software
```bash
# Python and pip
python3 --version  # Should be 3.9+
pip3 --version     # Should be 21+

# Git (optional, for version control)
git --version
```

### API Keys Required
- **Anthropic API Key**: Get from https://console.anthropic.com/api_keys

---

## Installation

### Step 1: Clone or Download Project

```bash
# Navigate to project directory
cd /home/ubuntu/Desktop/LoanApplication
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Verify activation (should show (venv) prefix)
which python
```

### Step 3: Install Dependencies

```bash
# Upgrade pip, setuptools, wheel
pip install --upgrade pip setuptools wheel

# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "streamlit|fastapi|pydantic|anthropic"
```

### Step 4: Create Environment File

```bash
# Copy template
cp .env.example .env

# Edit with your API key
nano .env

# Add your API key:
# ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

### Step 5: Verify Setup

```bash
# Check Python packages
python -c "import streamlit; import fastapi; import pydantic; print('✅ All packages installed')"

# Check .env file
cat .env | grep ANTHROPIC_API_KEY
```

---

## Configuration

### Environment Variables (.env)

```bash
# API Configuration
ANTHROPIC_API_KEY=your_api_key_here
MODEL_NAME=claude-opus-5-5-20250805

# Service Ports
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
STREAMLIT_PORT=8501

# MCP Servers
MCP_APPLICANT_DB_URL=http://localhost:8001
MCP_RISK_RULES_URL=http://localhost:8002
MCP_DECISION_SYNTHESIS_URL=http://localhost:8003
MCP_NOTIFICATION_URL=http://localhost:8004

# Decision Rules
APPROVED_THRESHOLD=0.7
REVIEW_THRESHOLD=0.4
CONFIDENCE_THRESHOLD=0.6

# Loan Limits
MIN_LOAN_AMOUNT=50000
MAX_LOAN_AMOUNT=5000000
MAX_DTI_RATIO=0.5

# Credit Scores
EXCELLENT_CREDIT=750
GOOD_CREDIT=700
FAIR_CREDIT=650
POOR_CREDIT=600
```

### Configuration File (config/settings.py)

See `config/settings.py` for all configuration options including risk thresholds, credit score bands, and loan limits.

---

## Running the Application

### Option 1: Automated (Recommended)

```bash
# Make script executable
chmod +x start_all_services.sh

# Run all services
./start_all_services.sh

# Services will start on:
# - ApplicantDB: http://localhost:8001
# - RiskRulesDB: http://localhost:8002
# - DecisionSynthesis: http://localhost:8003
# - NotificationSystem: http://localhost:8004
# - FastAPI: http://localhost:8000
# - Streamlit: http://localhost:8501
```

### Option 2: Manual (Open 6 Terminals)

**Terminal 1 - ApplicantDB MCP Server:**
```bash
source venv/bin/activate
python -m mcp_servers.applicant_db
```

**Terminal 2 - RiskRulesDB MCP Server:**
```bash
source venv/bin/activate
python -m mcp_servers.risk_rules_db
```

**Terminal 3 - DecisionSynthesis MCP Server:**
```bash
source venv/bin/activate
python -m mcp_servers.decision_synthesis
```

**Terminal 4 - NotificationSystem MCP Server:**
```bash
source venv/bin/activate
python -m mcp_servers.notification_system
```

**Terminal 5 - FastAPI Microservice:**
```bash
source venv/bin/activate
python -m services.microservice
```

**Terminal 6 - Streamlit UI:**
```bash
source venv/bin/activate
streamlit run ui/streamlit_app.py --server.port=8501
```

### Option 3: Docker (Future)

```bash
# Build Docker image
docker build -t ai-agent-loan-approval .

# Run with Docker Compose
docker-compose up
```

---

## Health Check

### Check All Services

```bash
# Check FastAPI
curl http://localhost:8000/health

# Check ApplicantDB
curl http://localhost:8001/health

# Check RiskRulesDB
curl http://localhost:8002/health

# Check DecisionSynthesis
curl http://localhost:8003/health

# Check NotificationSystem
curl http://localhost:8004/health

# Check Streamlit
curl http://localhost:8501
```

### Expected Response
```json
{
  "status": "healthy",
  "service": "Service Name"
}
```

---

## Database Setup

### Current Setup: In-Memory Storage
- Data stored in RAM
- Lost on application restart
- Good for development and testing

### Production Setup Options

#### Option 1: SQLite (File-based)
```bash
# Install
pip install SQLAlchemy

# Add to .env
DATABASE_URL=sqlite:///./loan_applications.db
```

#### Option 2: PostgreSQL (Recommended)
```bash
# Install PostgreSQL
sudo apt-get install postgresql

# Start service
sudo service postgresql start

# Create database
createdb loan_db
createuser loanuser

# Set password
psql -U postgres -c "ALTER USER loanuser WITH PASSWORD 'password';"

# Add to .env
DATABASE_URL=postgresql://loanuser:password@localhost:5432/loan_db

# Install Python driver
pip install psycopg2-binary SQLAlchemy
```

#### Option 3: MongoDB
```bash
# Install MongoDB
sudo apt-get install mongodb

# Start service
sudo service mongod start

# Add to .env
DATABASE_URL=mongodb://localhost:27017/loan_db

# Install Python driver
pip install pymongo
```

---

## API Documentation

### Interactive API Docs
Open: `http://localhost:8000/docs`

### REST Endpoints

#### Submit Loan Application
```
POST /api/apply
Content-Type: application/json

{
  "applicant_id": "APPL-001",
  "age": 35,
  "income": 75000,
  "employment_type": "full_time",
  "credit_score": 720,
  "loan_amount": 250000,
  "loan_tenure_months": 60,
  "existing_liabilities": 50000,
  "location": "California"
}

Response:
{
  "applicant_id": "APPL-001",
  "decision": "Approved",
  "risk_score": 0.30,
  "confidence_level": 0.87,
  "explanation": "...",
  "key_factors": [...],
  "case_id": "CASE-ABC123",
  "timestamp": "2026-11-10T09:30:00"
}
```

#### Check Application Status
```
GET /api/status/{applicant_id}

Response:
{
  "application": {...},
  "response": {...},
  "submitted_at": "2026-11-10T09:30:00"
}
```

#### List All Applications
```
GET /api/applications

Response:
{
  "total": 5,
  "applications": ["APPL-001", "APPL-002", ...]
}
```

#### Health Check
```
GET /health

Response:
{
  "status": "healthy",
  "service": "Loan Approval Microservice",
  "applications_processed": 5
}
```

---

## Testing

### Manual Testing via Web UI

1. **Open Application**
   ```
   http://localhost:8501
   ```

2. **Submit Test Application**
   - Click "New Application" tab
   - Fill in form fields
   - Click "🚀 Submit Application"

3. **View Decision**
   - Large colored status header (Green/Red/Yellow)
   - Decision summary with metrics
   - Detailed analysis

### Test Data

**For APPROVED Decision:**
```
Applicant ID: TEST-APPROVED
Age: 35
Income: $75,000
Employment: full_time
Credit Score: 720
Loan Amount: $250,000
Tenure: 60 months
Liabilities: $50,000
Location: California
```

**For REQUIRES MANUAL REVIEW:**
```
Applicant ID: TEST-REVIEW
Age: 42
Income: $60,000
Employment: part_time
Credit Score: 680
Loan Amount: $200,000
Tenure: 84 months
Liabilities: $80,000
Location: Texas
```

**For REJECTED Decision:**
```
Applicant ID: TEST-REJECTED
Age: 55
Income: $40,000
Employment: self_employed
Credit Score: 580
Loan Amount: $300,000
Tenure: 120 months
Liabilities: $150,000
Location: Nevada
```

### API Testing with curl

```bash
# Submit application
curl -X POST http://localhost:8000/api/apply \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "TEST-001",
    "age": 35,
    "income": 75000,
    "employment_type": "full_time",
    "credit_score": 720,
    "loan_amount": 250000,
    "loan_tenure_months": 60,
    "existing_liabilities": 50000,
    "location": "California"
  }'

# Check status
curl http://localhost:8000/api/status/TEST-001

# List all
curl http://localhost:8000/api/applications
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8501

# Kill process
kill -9 <PID>

# Alternative: change port in .env
STREAMLIT_PORT=8502
```

### Module Not Found Error

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify installation
python -c "import streamlit; import fastapi; print('OK')"
```

### API Key Error

```bash
# Verify API key in .env
cat .env | grep ANTHROPIC_API_KEY

# Get new key from
https://console.anthropic.com/api_keys

# Update .env
nano .env
```

### Services Not Responding

```bash
# Check if services are running
ps aux | grep python

# Check port availability
netstat -tuln | grep 850

# Restart all services
pkill -f streamlit
pkill -f uvicorn
pkill -f mcp_servers

# Start again
./start_all_services.sh
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -U loanuser -d loan_db -h localhost

# Test MongoDB connection
mongo mongodb://localhost:27017/loan_db

# Check .env DATABASE_URL
cat .env | grep DATABASE_URL
```

---

## Project Structure

```
LoanApplication/
├── config/
│   ├── settings.py           # Configuration constants
│   └── __init__.py
├── agents/
│   ├── applicant_agent.py    # Applicant Profile Analysis
│   ├── risk_agent.py         # Financial Risk Assessment
│   ├── decision_agent.py     # Loan Decision Making
│   ├── compliance_agent.py   # Compliance & Notifications
│   └── __init__.py
├── mcp_servers/
│   ├── applicant_db.py       # ApplicantDB MCP Server
│   ├── risk_rules_db.py      # RiskRulesDB MCP Server
│   ├── decision_synthesis.py # DecisionSynthesis MCP Server
│   ├── notification_system.py# NotificationSystem MCP Server
│   └── __init__.py
├── orchestrator/
│   ├── langgraph_engine.py   # LangGraph Orchestration
│   └── __init__.py
├── services/
│   ├── microservice.py       # FastAPI Microservice
│   └── __init__.py
├── models/
│   ├── loan_application.py   # Pydantic Models
│   └── __init__.py
├── ui/
│   └── streamlit_app.py      # Streamlit UI
├── utils/
│   ├── llm.py                # LLM Client Wrapper
│   ├── logger.py             # Logging Configuration
│   └── __init__.py
├── tests/
│   └── __init__.py
├── .env.example              # Environment Template
├── requirements.txt          # Python Dependencies
├── start_all_services.sh     # Automated Launcher
├── README.md                 # Full Documentation
├── SETUP_GUIDE.md            # Setup Instructions
└── CREATE.md                 # This File
```

---

## Support & Resources

- **Documentation**: See README.md for comprehensive docs
- **Setup Help**: See SETUP_GUIDE.md for detailed setup
- **Quick Start**: See QUICK_START.txt for quick reference
- **API Docs**: http://localhost:8000/docs (when running)
- **Health Status**: http://localhost:8000/health

---

## Next Steps

1. ✅ Complete installation
2. ✅ Configure .env with API key
3. ✅ Run `./start_all_services.sh`
4. ✅ Open http://localhost:8501
5. ✅ Submit test loan application
6. ✅ View AI decision

---

**Happy loan approving! 🎉**

For questions or issues, refer to the comprehensive documentation in README.md and SETUP_GUIDE.md.
