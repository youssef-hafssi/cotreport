#!/usr/bin/env python3
"""
USD Index COT Report Analyzer
Collects and analyzes CFTC Commitments of Traders data for USD Index
to provide directional bias insights.
"""

import requests
import re
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class USDIndexCOTAnalyzer:
    def __init__(self):
        self.url = "https://www.cftc.gov/dea/futures/deanybtlf.htm"
        self.data = {}
        self.analysis_results = {}
        
    def fetch_cot_data(self) -> str:
        """Fetch the latest COT report from CFTC website."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch COT data: {e}")
    
    def parse_usd_index_data(self, html_content: str) -> Dict:
        """Extract USD Index specific data from the COT report."""
        # Find USD INDEX section
        usd_pattern = r'USD INDEX - ICE FUTURES U\.S\.(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)'
        usd_match = re.search(usd_pattern, html_content, re.DOTALL)

        if not usd_match:
            raise Exception("USD Index data not found in COT report")

        usd_section = usd_match.group(1)

        # Extract report date - more flexible pattern
        date_pattern = r'(\w+) (\d+), (\d+)'
        date_match = re.search(date_pattern, usd_section)
        if date_match:
            month, day, year = date_match.groups()
            report_date = f"{day}/{month[:3]}/{year}"
        else:
            report_date = "Unknown"

        # Extract position data using regex patterns
        data_lines = usd_section.split('\n')

        # Find the main data line (All positions) - more flexible matching
        all_line = None
        for line in data_lines:
            stripped = line.strip()
            if stripped.startswith('All') and ':' in stripped:
                all_line = line
                break

        if not all_line:
            # Try alternative patterns
            for line in data_lines:
                if 'All' in line and any(char.isdigit() for char in line):
                    all_line = line
                    break

        if not all_line:
            raise Exception("Could not find position data in USD Index section")

        # Parse the position numbers - more robust extraction
        # Remove commas and extract all numbers
        clean_line = all_line.replace(',', '')
        numbers = re.findall(r'\d+', clean_line)
        numbers = [int(n) for n in numbers]

        # Extract changes line - look for line with negative numbers
        changes_line = None
        for line in data_lines:
            if 'Changes in Commitments from:' in line:
                # Find the next line with actual change data
                line_idx = data_lines.index(line)
                if line_idx + 1 < len(data_lines):
                    next_line = data_lines[line_idx + 1]
                    if ':' in next_line and any(c in next_line for c in ['-', '+']):
                        changes_line = next_line
                        break

        changes = []
        if changes_line:
            # More careful parsing of changes - extract numbers with signs
            clean_changes = changes_line.replace(',', '')
            # Find all signed numbers
            change_numbers = re.findall(r'-?\d+', clean_changes)
            # Skip the first number (total change) and take the position changes
            if len(change_numbers) > 1:
                changes = [int(x) for x in change_numbers[1:]]  # Skip first number

        return {
            'report_date': report_date,
            'total_open_interest': numbers[0] if numbers else 0,
            'non_commercial_long': numbers[1] if len(numbers) > 1 else 0,
            'non_commercial_short': numbers[2] if len(numbers) > 2 else 0,
            'spreading': numbers[3] if len(numbers) > 3 else 0,
            'commercial_long': numbers[4] if len(numbers) > 4 else 0,
            'commercial_short': numbers[5] if len(numbers) > 5 else 0,
            'total_long': numbers[6] if len(numbers) > 6 else 0,
            'total_short': numbers[7] if len(numbers) > 7 else 0,
            'nonreportable_long': numbers[8] if len(numbers) > 8 else 0,
            'nonreportable_short': numbers[9] if len(numbers) > 9 else 0,
            'changes': changes[:10] if len(changes) >= 10 else changes
        }
    
    def calculate_metrics(self, data: Dict) -> Dict:
        """Calculate key COT metrics for analysis."""
        metrics = {}
        
        # Net positions
        metrics['non_commercial_net'] = data['non_commercial_long'] - data['non_commercial_short']
        metrics['commercial_net'] = data['commercial_long'] - data['commercial_short']
        
        # Percentages of open interest
        total_oi = data['total_open_interest']
        if total_oi > 0:
            metrics['non_commercial_long_pct'] = (data['non_commercial_long'] / total_oi) * 100
            metrics['non_commercial_short_pct'] = (data['non_commercial_short'] / total_oi) * 100
            metrics['commercial_long_pct'] = (data['commercial_long'] / total_oi) * 100
            metrics['commercial_short_pct'] = (data['commercial_short'] / total_oi) * 100
        
        # Sentiment ratios
        if data['non_commercial_short'] > 0:
            metrics['non_commercial_ratio'] = data['non_commercial_long'] / data['non_commercial_short']
        
        if data['commercial_short'] > 0:
            metrics['commercial_ratio'] = data['commercial_long'] / data['commercial_short']
        
        # Weekly changes (if available)
        if data['changes'] and len(data['changes']) >= 4:
            metrics['nc_long_change'] = data['changes'][1] if len(data['changes']) > 1 else 0
            metrics['nc_short_change'] = data['changes'][2] if len(data['changes']) > 2 else 0
            metrics['nc_net_change'] = metrics['nc_long_change'] - metrics['nc_short_change']
        
        return metrics
    
    def analyze_directional_bias(self, data: Dict, metrics: Dict) -> Dict:
        """Analyze the data to determine directional bias."""
        analysis = {
            'overall_bias': 'NEUTRAL',
            'confidence': 'LOW',
            'signals': [],
            'key_observations': []
        }
        
        bullish_signals = 0
        bearish_signals = 0
        
        # 1. Non-Commercial Net Position Analysis
        nc_net = metrics['non_commercial_net']
        if nc_net > 5000:  # Significantly net long
            analysis['signals'].append("Large speculators (non-commercial) are net LONG - BULLISH signal")
            bullish_signals += 2
        elif nc_net < -5000:  # Significantly net short
            analysis['signals'].append("Large speculators (non-commercial) are net SHORT - BEARISH signal")
            bearish_signals += 2
        
        # 2. Commercial vs Non-Commercial Positioning
        comm_net = metrics['commercial_net']
        if nc_net > 0 and comm_net < 0:
            analysis['signals'].append("Speculators LONG vs Commercials SHORT - Classic BULLISH setup")
            bullish_signals += 1
        elif nc_net < 0 and comm_net > 0:
            analysis['signals'].append("Speculators SHORT vs Commercials LONG - Classic BEARISH setup")
            bearish_signals += 1
        
        # 3. Extreme Positioning Analysis
        nc_long_pct = metrics.get('non_commercial_long_pct', 0)
        nc_short_pct = metrics.get('non_commercial_short_pct', 0)
        
        if nc_long_pct > 50:
            analysis['signals'].append(f"High speculative long interest ({nc_long_pct:.1f}%) - Strong BULLISH sentiment")
            bullish_signals += 1
        elif nc_short_pct > 50:
            analysis['signals'].append(f"High speculative short interest ({nc_short_pct:.1f}%) - Strong BEARISH sentiment")
            bearish_signals += 1
        
        # 4. Weekly Changes Analysis
        if 'nc_net_change' in metrics:
            nc_change = metrics['nc_net_change']
            if nc_change > 1000:
                analysis['signals'].append(f"Large increase in speculative net long positions (+{nc_change}) - BULLISH momentum")
                bullish_signals += 1
            elif nc_change < -1000:
                analysis['signals'].append(f"Large decrease in speculative net positions ({nc_change}) - BEARISH momentum")
                bearish_signals += 1
        
        # 5. Ratio Analysis
        if 'non_commercial_ratio' in metrics:
            nc_ratio = metrics['non_commercial_ratio']
            if nc_ratio > 1.5:
                analysis['signals'].append(f"Strong long/short ratio ({nc_ratio:.2f}) - BULLISH bias")
                bullish_signals += 1
            elif nc_ratio < 0.7:
                analysis['signals'].append(f"Weak long/short ratio ({nc_ratio:.2f}) - BEARISH bias")
                bearish_signals += 1
        
        # Determine overall bias
        signal_diff = bullish_signals - bearish_signals
        
        if signal_diff >= 3:
            analysis['overall_bias'] = 'STRONGLY BULLISH'
            analysis['confidence'] = 'HIGH'
        elif signal_diff >= 1:
            analysis['overall_bias'] = 'BULLISH'
            analysis['confidence'] = 'MEDIUM' if signal_diff >= 2 else 'LOW'
        elif signal_diff <= -3:
            analysis['overall_bias'] = 'STRONGLY BEARISH'
            analysis['confidence'] = 'HIGH'
        elif signal_diff <= -1:
            analysis['overall_bias'] = 'BEARISH'
            analysis['confidence'] = 'MEDIUM' if signal_diff <= -2 else 'LOW'
        else:
            analysis['overall_bias'] = 'NEUTRAL'
            analysis['confidence'] = 'LOW'
        
        # Key observations
        analysis['key_observations'] = [
            f"Total Open Interest: {data['total_open_interest']:,} contracts",
            f"Non-Commercial Net Position: {nc_net:,} contracts",
            f"Commercial Net Position: {comm_net:,} contracts",
            f"Speculative Long %: {nc_long_pct:.1f}%",
            f"Speculative Short %: {nc_short_pct:.1f}%"
        ]
        
        return analysis
    
    def run_analysis(self) -> Dict:
        """Run the complete COT analysis."""
        print("🔄 Fetching latest USD Index COT data...")
        html_content = self.fetch_cot_data()
        
        print("📊 Parsing USD Index data...")
        self.data = self.parse_usd_index_data(html_content)
        
        print("🧮 Calculating metrics...")
        metrics = self.calculate_metrics(self.data)
        
        print("🎯 Analyzing directional bias...")
        self.analysis_results = self.analyze_directional_bias(self.data, metrics)
        
        return {
            'data': self.data,
            'metrics': metrics,
            'analysis': self.analysis_results
        }
    
    def print_report(self):
        """Print a formatted analysis report."""
        if not self.data or not self.analysis_results:
            print("❌ No analysis data available. Run analysis first.")
            return
        
        print("\n" + "="*60)
        print("🇺🇸 USD INDEX COT ANALYSIS REPORT")
        print("="*60)
        print(f"📅 Report Date: {self.data['report_date']}")
        print(f"🎯 Overall Bias: {self.analysis_results['overall_bias']}")
        print(f"🔍 Confidence: {self.analysis_results['confidence']}")
        
        print(f"\n📈 KEY METRICS:")
        print("-" * 30)
        for obs in self.analysis_results['key_observations']:
            print(f"  • {obs}")
        
        print(f"\n🚦 SIGNALS DETECTED:")
        print("-" * 30)
        if self.analysis_results['signals']:
            for i, signal in enumerate(self.analysis_results['signals'], 1):
                print(f"  {i}. {signal}")
        else:
            print("  • No significant signals detected")
        
        print(f"\n💡 TRADING IMPLICATIONS:")
        print("-" * 30)
        bias = self.analysis_results['overall_bias']
        confidence = self.analysis_results['confidence']
        
        if 'BULLISH' in bias:
            print("  • Consider LONG USD Index positions")
            print("  • Look for pullbacks as buying opportunities")
            print("  • Monitor for trend continuation patterns")
        elif 'BEARISH' in bias:
            print("  • Consider SHORT USD Index positions")
            print("  • Look for rallies as selling opportunities")
            print("  • Monitor for breakdown patterns")
        else:
            print("  • Neutral positioning recommended")
            print("  • Wait for clearer directional signals")
            print("  • Consider range-bound trading strategies")
        
        if confidence == 'LOW':
            print("  ⚠️  LOW confidence - Use smaller position sizes")
        elif confidence == 'HIGH':
            print("  ✅ HIGH confidence - Signals align strongly")
        
        print("\n" + "="*60)
        print("⚠️  DISCLAIMER: This analysis is for educational purposes only.")
        print("   Always conduct your own research before trading.")
        print("="*60)

def main():
    """Main execution function."""
    try:
        analyzer = USDIndexCOTAnalyzer()
        results = analyzer.run_analysis()
        analyzer.print_report()
        
        return results
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return None

if __name__ == "__main__":
    main()
