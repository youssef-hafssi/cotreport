# PowerShell script to setup backend only
# Run this from the backend directory

Write-Host "🔧 Setting up Multi-Asset COT Analyzer Backend..." -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Check if we're in the backend directory
if (-Not (Test-Path "app.py")) {
    Write-Host "❌ app.py not found. Please run this script from the backend directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Python is installed
Write-Host "🐍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment if it doesn't exist
if (-Not (Test-Path "venv")) {
    Write-Host "📦 Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if (-Not (Test-Path "venv")) {
        Write-Host "❌ Failed to create virtual environment." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
} else {
    Write-Host "✅ Virtual environment already exists." -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies
if (Test-Path "requirements.txt") {
    Write-Host "📥 Installing Python dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host "📥 Installing basic Python dependencies..." -ForegroundColor Yellow
    pip install flask flask-cors requests pandas numpy
}

Write-Host ""
Write-Host "✅ Backend setup completed successfully!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 To start the backend server:" -ForegroundColor White
Write-Host "   python app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Server will be available at: http://localhost:5000" -ForegroundColor White
