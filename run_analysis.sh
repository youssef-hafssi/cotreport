#!/bin/bash

# USD Index COT Analysis Runner
# Simple script to run the COT analysis with virtual environment

echo "🚀 Starting USD Index COT Analysis..."
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    
    echo "📥 Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "✅ Virtual environment found"
    source venv/bin/activate
fi

# Run the analysis
echo ""
echo "🔄 Running COT analysis..."
python usd_index_cot_analyzer.py

echo ""
echo "✅ Analysis complete!"
echo "📁 Check the generated files:"
echo "   - cot_analysis_results.json (detailed data)"
echo "   - cot_summary.txt (summary)"

deactivate
