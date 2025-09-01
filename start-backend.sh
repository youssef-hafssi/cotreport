#!/bin/bash

echo "🐍 Starting Multi-Asset COT Analyzer Backend..."
echo "==============================================="

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if required Python packages are installed
echo "📦 Checking dependencies..."
python -c "import flask, flask_cors, requests, pandas, numpy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Missing dependencies. Installing..."
    pip install -r requirements.txt
fi

# Start the Flask server
echo "🚀 Starting Flask API server..."
echo "📡 Server will be available at: http://localhost:5000"
echo "🔗 API endpoints:"
echo "   GET  /api/health  - Health check"
echo "   GET  /api/status  - System status"
echo "   GET  /api/assets  - Get available assets"
echo "   POST /api/analyze - Run COT analysis for selected asset"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================="

python app.py
