# PowerShell script to start Multi-Asset COT Analyzer Frontend

Write-Host "⚛️  Starting Multi-Asset COT Analyzer Frontend..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Check if Node.js is installed
Write-Host "📦 Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Found Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 16+ from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check if package.json exists
if (-Not (Test-Path "package.json")) {
    Write-Host "❌ package.json not found. Please run setup.ps1 first." -ForegroundColor Red
    exit 1
}

# Check if node_modules exists
if (-Not (Test-Path "node_modules")) {
    Write-Host "📥 Installing Node.js dependencies..." -ForegroundColor Yellow
    npm install
}

# Start the React development server
Write-Host "🚀 Starting React development server..." -ForegroundColor Green
Write-Host "🌐 Frontend will be available at: http://localhost:3000" -ForegroundColor White
Write-Host "🔗 Make sure the backend is running at: http://localhost:5000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan

npm start
