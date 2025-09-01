#!/usr/bin/env python3
"""
Flask API backend for USD Index COT Analyzer
Provides REST API endpoints for the React frontend
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
import traceback

# Add the parent directory to the path to import our analyzer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from multi_asset_cot_analyzer import MultiAssetCOTAnalyzer
except ImportError as e:
    print(f"Error importing MultiAssetCOTAnalyzer: {e}")
    print("Make sure multi_asset_cot_analyzer.py is in the parent directory")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'USD Index COT Analyzer API is running'
    })

@app.route('/api/assets', methods=['GET'])
def get_available_assets():
    """
    Get list of available assets for analysis
    """
    try:
        analyzer = MultiAssetCOTAnalyzer()
        assets = analyzer.get_available_assets()
        return jsonify({
            'assets': assets,
            'total_count': len(assets)
        })
    except Exception as e:
        return jsonify({
            'error': f'Failed to get assets: {str(e)}'
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_cot():
    """
    Run COT analysis for specified asset
    """
    try:
        # Get request data
        data = request.get_json() or {}
        asset_name = data.get('asset', 'USD INDEX')

        # Create analyzer instance
        analyzer = MultiAssetCOTAnalyzer()

        # Run the analysis for specified asset
        results = analyzer.run_analysis(asset_name)

        # Return the results as JSON
        return jsonify(results)

    except Exception as e:
        # Log the full error for debugging
        print(f"Error during analysis: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")

        # Return error response
        return jsonify({
            'error': f'Analysis failed: {str(e)}',
            'details': 'Please check the server logs for more information'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """
    Get current system status and information
    """
    try:
        return jsonify({
            'status': 'operational',
            'analyzer_available': True,
            'data_source': 'https://www.cftc.gov/dea/futures/deanybtlf.htm',
            'update_frequency': 'Weekly (typically Friday afternoons)',
            'last_check': 'Available on demand'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'analyzer_available': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested API endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred on the server'
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Multi-Asset COT Analyzer API...")
    print("📊 Available endpoints:")
    print("   GET  /api/health  - Health check")
    print("   GET  /api/status  - System status")
    print("   GET  /api/assets  - Get available assets")
    print("   POST /api/analyze - Run COT analysis for selected asset")
    print("🌐 Server will be available at: http://localhost:5000")
    print("🔗 React app should be configured to proxy to this server")
    print("-" * 50)
    
    # Run the Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
