@echo off
echo 🔧 Setting up Multi-Asset COT Analyzer Backend...
echo =================================================

REM Check if we're in the backend directory
if not exist "app.py" (
    echo ❌ app.py not found. Please run this script from the backend directory.
    pause
    exit /b 1
)

REM Check if Python is installed
echo 🐍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
) else (
    echo ✅ Python found
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
    if not exist "venv" (
        echo ❌ Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo ✅ Virtual environment already exists.
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
if exist "requirements.txt" (
    echo 📥 Installing Python dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo 📥 Installing basic Python dependencies...
    pip install flask flask-cors requests pandas numpy
)

echo.
echo ✅ Backend setup completed successfully!
echo =======================================
echo.
echo 🚀 To start the backend server:
echo    python app.py
echo.
echo 🌐 Server will be available at: http://localhost:5000
pause
