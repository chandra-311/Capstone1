#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║            🚀 STARTING LOAN APPROVAL SYSTEM - HEADLESS MODE 🚀            ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

SERVICE_PIDS=()

cleanup() {
    echo ""
    echo "🛑 Shutting down all services..."
    for pid in "${SERVICE_PIDS[@]}"; do
        kill $pid 2>/dev/null
    done
    wait
    echo "✅ All services stopped"
}

trap cleanup EXIT

echo "📊 Starting MCP Servers..."

# Start MCP Servers
python -m mcp_servers.applicant_db > /tmp/applicant_db.log 2>&1 &
SERVICE_PIDS+=($!)
echo "  ✓ ApplicantDB (8001)"

python -m mcp_servers.risk_rules_db > /tmp/risk_rules.log 2>&1 &
SERVICE_PIDS+=($!)
echo "  ✓ RiskRulesDB (8002)"

python -m mcp_servers.decision_synthesis > /tmp/decision_synthesis.log 2>&1 &
SERVICE_PIDS+=($!)
echo "  ✓ DecisionSynthesis (8003)"

python -m mcp_servers.notification_system > /tmp/notification.log 2>&1 &
SERVICE_PIDS+=($!)
echo "  ✓ NotificationSystem (8004)"

echo "⏳ Waiting for MCP servers to initialize..."
sleep 3

echo ""
echo "🔌 Starting FastAPI Microservice..."
python -m services.microservice > /tmp/fastapi.log 2>&1 &
SERVICE_PIDS+=($!)
echo "  ✓ FastAPI (8000)"

sleep 2

echo ""
echo "🎨 Starting Streamlit UI (Headless Mode)..."
streamlit run ui/streamlit_app.py \
    --server.headless=true \
    --server.port=8501 \
    --logger.level=off \
    --client.showErrorDetails=false \
    > /tmp/streamlit.log 2>&1 &
STREAMLIT_PID=$!
SERVICE_PIDS+=($STREAMLIT_PID)
echo "  ✓ Streamlit (8501)"

echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo "✅ ALL SERVICES STARTED SUCCESSFULLY!"
echo "════════════════════════════════════════════════════════════════════════════"
echo ""
echo "📊 SERVICE STATUS:"
echo "  ✓ ApplicantDB:         http://localhost:8001/health"
echo "  ✓ RiskRulesDB:         http://localhost:8002/health"
echo "  ✓ DecisionSynthesis:   http://localhost:8003/health"
echo "  ✓ NotificationSystem:  http://localhost:8004/health"
echo "  ✓ FastAPI:             http://localhost:8000/health"
echo "  ✓ Streamlit UI:        http://localhost:8501 (HEADLESS MODE)"
echo ""
echo "🌐 ACCESS THE APPLICATION:"
echo "  👉 Open in browser: http://localhost:8501"
echo ""
echo "📋 LOGS LOCATION:"
echo "  📄 ApplicantDB:     /tmp/applicant_db.log"
echo "  📄 RiskRulesDB:     /tmp/risk_rules.log"
echo "  📄 DecisionSynthesis: /tmp/decision_synthesis.log"
echo "  📄 NotificationSystem: /tmp/notification.log"
echo "  📄 FastAPI:         /tmp/fastapi.log"
echo "  📄 Streamlit:       /tmp/streamlit.log"
echo ""
echo "🛑 TO STOP ALL SERVICES:"
echo "  Press Ctrl+C"
echo ""
echo "════════════════════════════════════════════════════════════════════════════"
echo ""

wait
