#!/bin/bash

# Multi-Agent Loan Approval System - Launch Script
# This script activates the virtual environment and starts all services

set -e

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║          🏦 LAUNCHING LOAN APPROVAL SYSTEM 🏦                             ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if .env has API key
if grep -q "your-api-key-here" .env; then
    echo "⚠️  WARNING: ANTHROPIC_API_KEY not set in .env file!"
    echo "📝 Please edit .env and add your API key from https://console.anthropic.com/api_keys"
    echo ""
    echo "To continue with a test key, uncomment the line in .env"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "✅ Virtual environment activated"
echo ""

# Run the startup script
chmod +x start_all_services.sh
exec ./start_all_services.sh
