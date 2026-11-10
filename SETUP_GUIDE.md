# Setup & Running Guide

## Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
cd /home/ubuntu/Desktop/LoanApplication
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
# Get your API key from: https://console.anthropic.com/
```

### 3. Run All Services

#### Option A: Automated (Recommended)
```bash
chmod +x start_all_services.sh
./start_all_services.sh
```

#### Option B: Manual - Open 6 terminals and run in each:

**Terminal 1 - ApplicantDB MCP Server:**
```bash
cd /home/ubuntu/Desktop/LoanApplication
python -m mcp_servers.applicant_db
```

**Terminal 2 - RiskRulesDB MCP Server:**
```bash
cd /home/ubuntu/Desktop/LoanApplication
python -m mcp_servers.risk_rules_db
```

**Terminal 3 - DecisionSynthesis MCP Server:**
```bash
cd /home/ubuntu/Desktop/LoanApplication
python -m mcp_servers.decision_synthesis
```

**Terminal 4 - NotificationSystem MCP Server:**
```bash
cd /home/ubuntu/Desktop/LoanApplication
python -m mcp_servers.notification_system
```

**Terminal 5 - FastAPI Microservice:**
```bash
cd /home/ubuntu/Desktop/LoanApplication
python -m services.microservice
```

**Terminal 6 - Streamlit UI:**
```bash
cd /home/ubuntu/Desktop/LoanApplication
streamlit run ui/streamlit_app.py
```

## Verification

### Check all services are running:

1. **ApplicantDB** (port 8001):
   ```bash
   curl http://localhost:8001/health
   ```
   Expected: `{"status":"healthy","service":"ApplicantDB"}`

2. **RiskRulesDB** (port 8002):
   ```bash
   curl http://localhost:8002/health
   ```

3. **DecisionSynthesis** (port 8003):
   ```bash
   curl http://localhost:8003/health
   ```

4. **NotificationSystem** (port 8004):
   ```bash
   curl http://localhost:8004/health
   ```

5. **FastAPI** (port 8000):
   ```bash
   curl http://localhost:8000/health
   ```
   Open in browser: http://localhost:8000/docs

6. **Streamlit UI** (port 8501):
   Open in browser: http://localhost:8501

## Using the System

### Via Streamlit UI (Recommended)

1. Open http://localhost:8501 in your browser
2. Fill in the loan application form
3. Click "🚀 Submit Application"
4. View decision, risk score, and detailed analysis

### Via API (curl)

```bash
curl -X POST http://localhost:8000/api/apply \
  -H "Content-Type: application/json" \
  -d '{
    "applicant_id": "APPL-001",
    "age": 35,
    "income": 75000,
    "employment_type": "full_time",
    "credit_score": 720,
    "loan_amount": 250000,
    "loan_tenure_months": 60,
    "existing_liabilities": 50000,
    "location": "California"
  }'
```

### Check Application Status

```bash
curl http://localhost:8000/api/status/APPL-001
```

## Troubleshooting

### Port Already in Use
```bash
# Kill process on specific port (e.g., 8000)
lsof -ti:8000 | xargs kill -9
```

### Module Not Found Error
```bash
# Make sure you're in the correct directory
cd /home/ubuntu/Desktop/LoanApplication

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### API Key Error
```bash
# Verify .env file has ANTHROPIC_API_KEY
cat .env | grep ANTHROPIC_API_KEY

# Get your key from https://console.anthropic.com/api_keys
```

### MCP Server Connection Failed
```bash
# Make sure all MCP servers are running on ports 8001-8004
# Check they're listening:
netstat -tuln | grep -E '800[1-4]'
```

### Streamlit Not Loading
```bash
# Try accessing without https
http://localhost:8501

# Clear cache and restart
rm -rf ~/.streamlit/
streamlit run ui/streamlit_app.py --logger.level=debug
```

## Architecture Overview

```
┌─────────────────────┐
│  Streamlit UI       │ (http://localhost:8501)
│  📱 User Interface  │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│ FastAPI Service     │ (http://localhost:8000)
│ REST Endpoints      │
└──────────┬──────────┘
           │
┌──────────▼──────────────────────┐
│ LangGraph Orchestrator          │
│ Workflow Coordination           │
└─┬──────────┬──────────┬────────┬┘
  │          │          │        │
  ▼          ▼          ▼        ▼
┌─────────┐┌──────────┐┌──────────┐┌──────────┐
│ Applicant││Financial ││Loan      ││Compliance│
│ Profile ││Risk      ││Decision  ││& Action  │
│Agent    ││Agent     ││Agent     ││Agent     │
└────┬────┘└────┬─────┘└────┬─────┘└────┬─────┘
     │          │           │          │
     ▼          ▼           ▼          ▼
┌─────────┐┌──────────┐┌──────────┐┌──────────┐
│Applicant││RiskRules ││Decision  ││Notification
│DB MCP   ││DB MCP    ││Synthesis ││System MCP
└─────────┘└──────────┘└──────────┘└──────────┘
  :8001      :8002        :8003       :8004
```

## Next Steps

1. **Test with sample data** - Use "New Application" tab
2. **Check API docs** - Visit http://localhost:8000/docs
3. **Review decisions** - See "All Applications" tab
4. **Customize thresholds** - Edit `config/settings.py`
5. **Extend agents** - Add new agents in `agents/` directory

## System Workflow

1. User submits application via Streamlit
2. FastAPI validates and forwards to orchestrator
3. Orchestrator invokes all 4 agents in parallel where possible
4. Each agent queries its MCP server
5. Agents return analysis with scores and reasoning
6. Final decision synthesized (Approve/Reject/Review)
7. Compliance agent logs case and sends notifications
8. Decision returned to UI with full explanation

## Performance Notes

- First request: ~3-5 seconds (model initialization)
- Subsequent requests: ~2-3 seconds
- Can handle 10+ concurrent applications
- All decisions are logged and auditable

## Configuration

Edit `config/settings.py` to customize:

```python
# Decision thresholds (0-1 scale)
APPROVED_THRESHOLD = 0.7      # Risk score < 0.3 = Approve
REVIEW_THRESHOLD = 0.4        # Risk score 0.3-0.6 = Review
CONFIDENCE_THRESHOLD = 0.6    # Minimum confidence

# Loan limits
MIN_LOAN_AMOUNT = 50000
MAX_LOAN_AMOUNT = 5000000

# Financial rules
MAX_DTI_RATIO = 0.5           # Debt-to-Income ratio

# Credit score bands
EXCELLENT_CREDIT = 750
GOOD_CREDIT = 700
FAIR_CREDIT = 650
POOR_CREDIT = 600
```

## Support

Check these locations for debugging:

1. **Logs**: Console output from each service
2. **API Errors**: FastAPI docs at http://localhost:8000/docs
3. **UI Issues**: Browser console (F12)
4. **MCP Health**: Individual health endpoints

For detailed documentation, see [README.md](./README.md)
