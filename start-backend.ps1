# PowerShell script to start Multi-Asset COT Analyzer Backend

Write-Host "🐍 Starting Multi-Asset COT Analyzer Backend..." -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Check if we're in the root directory or backend directory
$currentDir = Get-Location
if (Test-Path "backend") {
    # We're in the root directory, navigate to backend
    Write-Host "📁 Navigating to backend directory..." -ForegroundColor Yellow
    Set-Location backend
} elseif (Test-Path "app.py") {
    # We're already in the backend directory
    Write-Host "📁 Already in backend directory..." -ForegroundColor Yellow
} else {
    Write-Host "❌ Cannot find backend directory or app.py. Please run from the project root or backend directory." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    Write-Host "💡 Or create it manually with: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Check if required Python packages are installed
Write-Host "📦 Checking dependencies..." -ForegroundColor Yellow
try {
    python -c "import flask, flask_cors, requests, pandas, numpy" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Dependencies missing"
    }
} catch {
    Write-Host "❌ Missing dependencies. Installing..." -ForegroundColor Red
    pip install -r requirements.txt
}

# Start the Flask server
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
