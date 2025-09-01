@echo off
echo 🐍 Starting Multi-Asset COT Analyzer Backend...
echo ===============================================

REM Navigate to backend directory
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if required Python packages are installed
echo 📦 Checking dependencies...
python -c "import flask, flask_cors, requests, pandas, numpy" >nul 2>&1
if errorlevel 1 (
    echo ❌ Missing dependencies. Installing...
    pip install -r requirements.txt
)

REM Start the Flask server
echo 🚀 Starting Flask API server...
echo 📡 Server will be available at: http://localhost:5000
echo 🔗 API endpoints:
echo    GET  /api/health  - Health check
echo    GET  /api/status  - System status
echo    GET  /api/assets  - Get available assets
echo    POST /api/analyze - Run COT analysis for selected asset
echo.
echo Press Ctrl+C to stop the server
echo =================================

python app.py
pause
