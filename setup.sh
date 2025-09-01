#!/bin/bash

# USD Index COT Analyzer - Full Stack Setup Script
echo "🚀 Setting up USD Index COT Analyzer Full Stack Application"
echo "=========================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ Python version: $(python3 --version)"
echo ""

# Setup Python backend
echo "🐍 Setting up Python backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📥 Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

cd ..

# Setup React frontend
echo "⚛️  Setting up React frontend..."
echo "📥 Installing Node.js dependencies..."
npm install

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🚀 To start the application:"
echo "   1. Start the Python backend:"
echo "      cd backend && source venv/bin/activate && python app.py"
echo ""
echo "   2. In a new terminal, start the React frontend:"
echo "      npm start"
echo ""
echo "   3. Open your browser to: http://localhost:3000"
echo ""
echo "📊 The app will automatically fetch and analyze USD Index COT data from CFTC"
echo "⚠️  Make sure both servers are running for the app to work properly"
