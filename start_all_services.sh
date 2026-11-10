#!/bin/bash

echo "=========================================="
echo "Multi-Agent Loan Approval System"
echo "Starting all services..."
echo "=========================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please update .env with your ANTHROPIC_API_KEY"
fi

# Function to run service in background
run_service() {
    local name=$1
    local port=$2
    local module=$3

    echo "🚀 Starting $name on port $port..."
    python -m $module &
    SERVICE_PIDS+=($!)
    sleep 2
}

# Array to store PIDs for cleanup
SERVICE_PIDS=()

# Trap for cleanup on exit
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

# Start MCP Servers
echo ""
echo "Starting MCP Servers..."
run_service "ApplicantDB" 8001 "mcp_servers.applicant_db"
run_service "RiskRulesDB" 8002 "mcp_servers.risk_rules_db"
run_service "DecisionSynthesis" 8003 "mcp_servers.decision_synthesis"
run_service "NotificationSystem" 8004 "mcp_servers.notification_system"

# Wait for MCP servers to start
echo "⏳ Waiting for MCP servers to initialize..."
sleep 3

# Start FastAPI Microservice
echo ""
echo "Starting FastAPI Microservice..."
run_service "FastAPI Microservice" 8000 "services.microservice"

# Wait for microservice to start
sleep 2

# Start Streamlit UI
echo ""
echo "🎨 Starting Streamlit UI..."
python -m streamlit run ui/streamlit_app.py --server.port=8501 &
STREAMLIT_PID=$!
SERVICE_PIDS+=($STREAMLIT_PID)

echo ""
echo "=========================================="
echo "✅ All services started successfully!"
echo "=========================================="
echo ""
echo "📊 Service URLs:"
echo "  - Streamlit UI: http://localhost:8501"
echo "  - FastAPI Docs: http://localhost:8000/docs"
echo "  - ApplicantDB: http://localhost:8001/health"
echo "  - RiskRulesDB: http://localhost:8002/health"
echo "  - DecisionSynthesis: http://localhost:8003/health"
echo "  - NotificationSystem: http://localhost:8004/health"
echo ""
echo "Press Ctrl+C to stop all services..."
echo ""

# Wait for all background processes
wait
