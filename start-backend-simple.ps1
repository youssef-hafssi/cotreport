# Simple PowerShell script to start Multi-Asset COT Analyzer Backend
# This script works from the backend directory

Write-Host "🐍 Starting Multi-Asset COT Analyzer Backend..." -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Check if we're in the correct directory
if (-Not (Test-Path "app.py")) {
    Write-Host "❌ app.py not found. Please run this script from the backend directory." -ForegroundColor Red
    Write-Host "💡 Navigate to the backend directory first: cd backend" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found." -ForegroundColor Red
    Write-Host "💡 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if (-Not (Test-Path "venv")) {
        Write-Host "❌ Failed to create virtual environment. Please check Python installation." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Check if requirements.txt exists and install dependencies
if (Test-Path "requirements.txt") {
    Write-Host "📦 Installing/updating dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host "📦 Installing basic dependencies..." -ForegroundColor Yellow
    pip install flask flask-cors requests pandas numpy
}

# Start the Flask server
Write-Host ""
Write-Host "🚀 Starting Flask API server..." -ForegroundColor Green
Write-Host "📡 Server will be available at: http://localhost:5000" -ForegroundColor White
Write-Host "🔗 API endpoints:" -ForegroundColor White
Write-Host "   GET  /api/health  - Health check" -ForegroundColor Gray
Write-Host "   GET  /api/status  - System status" -ForegroundColor Gray
Write-Host "   GET  /api/assets  - Get available assets" -ForegroundColor Gray
Write-Host "   POST /api/analyze - Run COT analysis for selected asset" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "=================================" -ForegroundColor Cyan

python app.py
