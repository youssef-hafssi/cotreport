#!/bin/bash

echo "⚛️  Starting USD Index COT Analyzer Frontend..."
echo "=============================================="

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ Node modules not found. Installing dependencies..."
    npm install
fi

echo "🚀 Starting React development server..."
echo "🌐 Frontend will be available at: http://localhost:3000"
echo "🔗 Make sure the backend is running at: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================="

npm start
