# PowerShell setup script for Multi-Asset COT Analyzer

Write-Host "🚀 Multi-Asset COT Analyzer Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "🐍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
Write-Host "📦 Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Found Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 16+ from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Backend Setup
Write-Host "🔧 Setting up Python backend..." -ForegroundColor Yellow

# Navigate to backend directory
if (-Not (Test-Path "backend")) {
    New-Item -ItemType Directory -Path "backend"
}
Set-Location backend

# Create virtual environment
if (-Not (Test-Path "venv")) {
    Write-Host "📦 Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install Python dependencies
if (Test-Path "requirements.txt") {
    Write-Host "📥 Installing Python dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host "⚠️  requirements.txt not found. Installing basic dependencies..." -ForegroundColor Yellow
    pip install flask flask-cors requests pandas numpy
}

# Return to root directory
Set-Location ..

# Frontend Setup
Write-Host "🎨 Setting up React frontend..." -ForegroundColor Yellow

# Install Node.js dependencies
if (Test-Path "package.json") {
    Write-Host "📥 Installing Node.js dependencies..." -ForegroundColor Yellow
    npm install
} else {
    Write-Host "⚠️  package.json not found. Skipping npm install..." -ForegroundColor Yellow
}

# Setup complete
Write-Host ""
Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 To start the application:" -ForegroundColor White
Write-Host "   1. Backend:  .\start-backend.ps1" -ForegroundColor Gray
Write-Host "   2. Frontend: npm start" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Application will be available at:" -ForegroundColor White
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Gray
Write-Host "   Backend:  http://localhost:5000" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 For more information, see README.md" -ForegroundColor White
