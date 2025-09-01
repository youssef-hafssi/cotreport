#!/usr/bin/env python3
"""
Multi-Asset COT Report Analyzer
Collects and analyzes CFTC Commitments of Traders data for multiple assets
from both USD Index and CME reports to provide directional bias insights.
"""

import requests
import re
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class MultiAssetCOTAnalyzer:
    def __init__(self):
        self.urls = {
            'usd_index': "https://www.cftc.gov/dea/futures/deanybtlf.htm",
            'cme': "https://www.cftc.gov/dea/futures/deacmelf.htm",
            'financial': "https://www.cftc.gov/dea/futures/financial_lf.htm"
        }
        self.data = {}
        self.analysis_results = {}
        
        # Define available assets with their patterns and sources
        self.available_assets = {
            # USD Index and ICE Futures
            'USD INDEX': {
                'source': 'usd_index',
                'pattern': r'USD INDEX - ICE FUTURES U\.S\.(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'US Dollar Index futures'
            },

            # Major Currency Pairs (Financial Futures)
            'BRITISH POUND': {
                'source': 'financial',
                'pattern': r'BRITISH POUND - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'British Pound futures (GBP/USD)'
            },
            'EURO FX': {
                'source': 'financial',
                'pattern': r'EURO FX - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'Euro FX futures (EUR/USD)'
            },
            'JAPANESE YEN': {
                'source': 'financial',
                'pattern': r'JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'Japanese Yen futures (JPY/USD)'
            },
            'CANADIAN DOLLAR': {
                'source': 'financial',
                'pattern': r'CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'Canadian Dollar futures (CAD/USD)'
            },
            'SWISS FRANC': {
                'source': 'financial',
                'pattern': r'SWISS FRANC - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'Swiss Franc futures (CHF/USD)'
            },
            'AUSTRALIAN DOLLAR': {
                'source': 'financial',
                'pattern': r'AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'Australian Dollar futures (AUD/USD)'
            },
            'NEW ZEALAND DOLLAR': {
                'source': 'financial',
                'pattern': r'NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'New Zealand Dollar futures (NZD/USD)'
            },
            'MEXICAN PESO': {
                'source': 'financial',
                'pattern': r'MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'Mexican Peso futures (MXN/USD)'
            },
            'BRAZILIAN REAL': {
                'source': 'financial',
                'pattern': r'BRAZILIAN REAL - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'Brazilian Real futures (BRL/USD)'
            },
            'SOUTH AFRICAN RAND': {
                'source': 'financial',
                'pattern': r'SO AFRICAN RAND - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'South African Rand futures (ZAR/USD)'
            },

            # Cryptocurrencies
            'BITCOIN': {
                'source': 'financial',
                'pattern': r'BITCOIN - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'Bitcoin futures'
            },
            'ETHEREUM': {
                'source': 'financial',
                'pattern': r'ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'Ethereum futures'
            },

            # Stock Indices
            'RUSSELL E-MINI': {
                'source': 'cme',
                'pattern': r'RUSSELL E-MINI - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Russell 2000 E-Mini futures'
            },
            'NIKKEI STOCK AVERAGE': {
                'source': 'cme',
                'pattern': r'NIKKEI STOCK AVERAGE YEN DENOM - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Nikkei Stock Average futures'
            },
            'S&P 500 ANNUAL DIVIDEND': {
                'source': 'cme',
                'pattern': r'S&P 500 ANNUAL DIVIDEND INDEX - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'S&P 500 Annual Dividend Index futures'
            },
            'DOW JONES': {
                'source': 'financial',
                'pattern': r'DJIA Consolidated - CHICAGO BOARD OF TRADE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'Dow Jones Industrial Average futures'
            },
            'VIX': {
                'source': 'financial',
                'pattern': r'VIX FUTURES - CBOE FUTURES EXCHANGE(.*?)(?=\n-{20,}|\nUpdated|\Z)',
                'description': 'VIX Volatility Index futures'
            },

            # Commodities - Agricultural
            'LEAN HOGS': {
                'source': 'cme',
                'pattern': r'LEAN HOGS - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Lean Hogs futures'
            },
            'LIVE CATTLE': {
                'source': 'cme',
                'pattern': r'LIVE CATTLE - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Live Cattle futures'
            },
            'MILK CLASS III': {
                'source': 'cme',
                'pattern': r'MILK, Class III - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Milk Class III futures'
            },
            'BUTTER': {
                'source': 'cme',
                'pattern': r'BUTTER \(CASH SETTLED\) - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Butter (Cash Settled) futures'
            },
            'NON FAT DRY MILK': {
                'source': 'cme',
                'pattern': r'NON FAT DRY MILK - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Non Fat Dry Milk futures'
            },

            # Commodities - ICE Futures
            'COTTON': {
                'source': 'usd_index',
                'pattern': r'COTTON NO\. 2 - ICE FUTURES U\.S\.(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Cotton No. 2 futures'
            },
            'SUGAR': {
                'source': 'usd_index',
                'pattern': r'SUGAR NO\. 11 - ICE FUTURES U\.S\.(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Sugar No. 11 futures'
            },
            'COFFEE': {
                'source': 'usd_index',
                'pattern': r'COFFEE C - ICE FUTURES U\.S\.(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Coffee C futures'
            },
            'COCOA': {
                'source': 'usd_index',
                'pattern': r'COCOA - ICE FUTURES U\.S\.(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Cocoa futures'
            },
            'ORANGE JUICE': {
                'source': 'usd_index',
                'pattern': r'FRZN CONCENTRATED ORANGE JUICE - ICE FUTURES U\.S\.(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Frozen Concentrated Orange Juice futures'
            },
            'CANOLA': {
                'source': 'usd_index',
                'pattern': r'CANOLA - ICE FUTURES U\.S\.(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Canola futures'
            },

            # Other
            'LUMBER': {
                'source': 'cme',
                'pattern': r'LUMBER - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Lumber futures'
            },
            'EURO SHORT TERM RATE': {
                'source': 'cme',
                'pattern': r'EURO SHORT TERM RATE - CHICAGO MERCANTILE EXCHANGE(.*?)(?=\n[A-Z][A-Z]|\nUpdated|\Z)',
                'description': 'Euro Short Term Rate futures'
            }
        }
        
    def get_available_assets(self) -> List[Dict]:
        """Return list of available assets for analysis."""
        assets = []
        for name, info in self.available_assets.items():
            assets.append({
                'name': name,
                'description': info['description'],
                'source': info['source']
            })
        return sorted(assets, key=lambda x: x['name'])

    def extract_current_cot_date(self, html_content: str) -> str:
        """Extract the current COT data date (should be the most recent Tuesday)."""
        from datetime import datetime, timedelta

        # Look for the main report date - this should be the current week's Tuesday
        main_date_patterns = [
            r'Commitments of Traders.*?as of (\w+) (\d+), (\d+)',
            r'COMMITMENTS OF TRADERS.*?(\w+) (\d+), (\d+)',
            r'Positions as of (\w+) (\d+), (\d+)',
        ]

        for pattern in main_date_patterns:
            match = re.search(pattern, html_content, re.IGNORECASE | re.DOTALL)
            if match:
                groups = match.groups()
                if len(groups) >= 3:
                    month, day, year = groups[-3:]  # Take last 3 groups
                    try:
                        # Verify this is a Tuesday (COT data is always for Tuesday)
                        date_obj = datetime.strptime(f"{month} {day}, {year}", "%B %d, %Y")
                        if date_obj.weekday() == 1:  # Tuesday is weekday 1
                            return f"{day}/{month[:3]}/{year}"
                    except ValueError:
                        continue

        # If no Tuesday found, get the most recent date that could be a Tuesday
        all_dates = re.findall(r'(\w+) (\d+), (\d+)', html_content)
        for month_str, day_str, year_str in reversed(all_dates):  # Start from most recent
            try:
                date_obj = datetime.strptime(f"{month_str} {day_str}, {year_str}", "%B %d, %Y")
                if date_obj.weekday() == 1:  # Tuesday
                    return f"{day_str}/{month_str[:3]}/{year_str}"
            except ValueError:
                continue

        return "Unknown"
        
    def fetch_cot_data(self, source: str) -> str:
        """Fetch the latest COT report from specified CFTC website."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            url = self.urls[source]
            print(f"🌐 Fetching from: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            # Debug: Check if we can find any dates in the content
            content = response.text
            date_matches = re.findall(r'(\w+) (\d+), (\d+)', content)
            if date_matches:
                print(f"📅 Dates found in report: {date_matches[:3]}...")  # Show first 3 dates

            return content
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch COT data from {source}: {e}")
    
    def parse_asset_data(self, html_content: str, asset_name: str) -> Dict:
        """Extract specific asset data from the COT report."""
        if asset_name not in self.available_assets:
            raise Exception(f"Asset '{asset_name}' not supported. Available assets: {list(self.available_assets.keys())}")

        asset_info = self.available_assets[asset_name]
        pattern = asset_info['pattern']
        source = asset_info['source']

        # Find asset section
        asset_match = re.search(pattern, html_content, re.DOTALL)

        if not asset_match:
            raise Exception(f"{asset_name} data not found in COT report")

        asset_section = asset_match.group(1)

        # Extract report date - use the improved method to get current COT date
        report_date = self.extract_current_cot_date(html_content)

        # Debug: Print what date we extracted
        print(f"🔍 Date extraction for {asset_name}: {report_date}")

        # Parse based on source type
        if source == 'financial':
            return self._parse_financial_data(asset_section, asset_name, report_date, html_content)
        else:
            return self._parse_standard_data(asset_section, asset_name, report_date)

    def _parse_financial_data(self, asset_section: str, asset_name: str, report_date: str, html_content: str = "") -> Dict:
        """Parse financial futures data format (different structure)."""
        data_lines = [line.strip() for line in asset_section.split('\n') if line.strip()]

        # Extract Open Interest and better date parsing for financial data
        total_oi = 0

        # Try to get a better date from the financial data
        if report_date == "Unknown" and html_content:
            # Financial reports have the date in the header
            financial_date_patterns = [
                r'Positions as of (\w+) (\d+), (\d+)',
                r'as of (\w+) (\d+), (\d+)',
                r'(\w+) (\d+), (\d+)'
            ]

            for pattern in financial_date_patterns:
                date_match = re.search(pattern, html_content, re.IGNORECASE)
                if date_match:
                    month, day, year = date_match.groups()
                    report_date = f"{day}/{month[:3]}/{year}"
                    break

        for line in data_lines:
            if 'Open Interest is' in line:
                oi_match = re.search(r'Open Interest is\s+(\d+(?:,\d+)*)', line)
                if oi_match:
                    total_oi = int(oi_match.group(1).replace(',', ''))
                break

        # Find the positions line - look for line with multiple numbers
        positions_line = None

        # Look for the line that starts with numbers (position data)
        # Financial format typically has a line with many comma-separated numbers
        for line in data_lines:
            # Skip header lines and look for data lines
            if (line and
                not line.startswith('CFTC Code') and
                not line.startswith('Positions') and
                not line.startswith('Changes') and
                not line.startswith('Percent') and
                not line.startswith('Number') and
                not 'Total Traders' in line and
                len(re.findall(r'\d+(?:,\d+)*', line)) >= 8):  # Line with many numbers
                positions_line = line
                break

        if not positions_line:
            # Try a more lenient approach - look for any line with lots of numbers
            for line in data_lines:
                numbers_in_line = re.findall(r'\d+(?:,\d+)*', line)
                if len(numbers_in_line) >= 6:  # At least 6 numbers
                    positions_line = line
                    break

        if not positions_line:
            # Last resort: try to find the first line after "Positions" that has numbers
            positions_found = False
            for line in data_lines:
                if 'Positions' in line:
                    positions_found = True
                    continue
                if positions_found and re.search(r'\d+', line):
                    positions_line = line
                    break

        if not positions_line:
            # Debug: print the section to understand the format
            print(f"DEBUG: Could not parse {asset_name}. Section content:")
            for i, line in enumerate(data_lines[:15]):  # Print first 15 lines
                print(f"Line {i}: '{line}'")
            raise Exception(f"Could not find position data in {asset_name} section")

        # Parse the position numbers - financial format has different columns
        clean_line = positions_line.replace(',', '')
        numbers = re.findall(r'\d+', clean_line)
        numbers = [int(n) for n in numbers]

        # Financial format: Dealer Long/Short/Spread, Asset Mgr Long/Short/Spread, Leveraged Long/Short/Spread, Other Long/Short/Spread, Nonreportable Long/Short
        # We'll map these to our standard format

        # Initialize default values
        non_commercial_long = 0
        non_commercial_short = 0
        commercial_long = 0
        commercial_short = 0
        nonreportable_long = 0
        nonreportable_short = 0

        if len(numbers) >= 10:
            # Try to map based on the financial format structure
            # Financial format typically has: Dealer, Asset Mgr, Leveraged, Other, Nonreportable
            # Each with Long, Short, Spreading columns

            try:
                # Assume standard financial format with 3 columns per category
                if len(numbers) >= 14:
                    # Full format: 5 categories × 3 columns (Long/Short/Spread) - 1 (no spread for nonreportable) = 14
                    dealer_long = numbers[0]
                    dealer_short = numbers[1]
                    asset_mgr_long = numbers[3]
                    asset_mgr_short = numbers[4]
                    leveraged_long = numbers[6]
                    leveraged_short = numbers[7]
                    other_long = numbers[9]
                    other_short = numbers[10]
                    nonreportable_long = numbers[12]
                    nonreportable_short = numbers[13]
                else:
                    # Simplified mapping for shorter arrays
                    leveraged_long = numbers[0] if len(numbers) > 0 else 0
                    leveraged_short = numbers[1] if len(numbers) > 1 else 0
                    dealer_long = numbers[2] if len(numbers) > 2 else 0
                    dealer_short = numbers[3] if len(numbers) > 3 else 0
                    asset_mgr_long = numbers[4] if len(numbers) > 4 else 0
                    asset_mgr_short = numbers[5] if len(numbers) > 5 else 0
                    other_long = numbers[6] if len(numbers) > 6 else 0
                    other_short = numbers[7] if len(numbers) > 7 else 0
                    nonreportable_long = numbers[8] if len(numbers) > 8 else 0
                    nonreportable_short = numbers[9] if len(numbers) > 9 else 0

                # Map to standard format - Leveraged Funds are the speculators (Non-Commercial)
                # Dealers + Asset Managers are more like Commercial hedgers
                non_commercial_long = leveraged_long + other_long  # Leveraged funds + other reportables
                non_commercial_short = leveraged_short + other_short
                commercial_long = dealer_long + asset_mgr_long  # Dealers + Asset managers
                commercial_short = dealer_short + asset_mgr_short

            except (IndexError, ValueError) as e:
                print(f"Warning: Error parsing {asset_name} financial data: {e}")
                # Use simple fallback
                non_commercial_long = numbers[0] if len(numbers) > 0 else 0
                non_commercial_short = numbers[1] if len(numbers) > 1 else 0
                commercial_long = numbers[2] if len(numbers) > 2 else 0
                commercial_short = numbers[3] if len(numbers) > 3 else 0
                nonreportable_long = numbers[4] if len(numbers) > 4 else 0
                nonreportable_short = numbers[5] if len(numbers) > 5 else 0

        else:
            # Very short array - use basic mapping
            non_commercial_long = numbers[0] if len(numbers) > 0 else 0
            non_commercial_short = numbers[1] if len(numbers) > 1 else 0
            commercial_long = numbers[2] if len(numbers) > 2 else 0
            commercial_short = numbers[3] if len(numbers) > 3 else 0
            nonreportable_long = numbers[4] if len(numbers) > 4 else 0
            nonreportable_short = numbers[5] if len(numbers) > 5 else 0

        # Use provided OI if available, otherwise estimate
        if total_oi == 0:
            total_oi = non_commercial_long + non_commercial_short + commercial_long + commercial_short + nonreportable_long + nonreportable_short
            if total_oi > 0:
                total_oi = total_oi // 2  # Divide by 2 since we're double counting (long + short)

        # Extract changes if available
        changes = []
        for line in data_lines:
            if 'Changes from:' in line:
                line_idx = data_lines.index(line)
                if line_idx + 1 < len(data_lines):
                    changes_line = data_lines[line_idx + 1]
                    clean_changes = changes_line.replace(',', '')
                    change_numbers = re.findall(r'-?\d+', clean_changes)
                    changes = [int(x) for x in change_numbers[:10]] if change_numbers else []
                break

        # Debug: Print what we extracted
        print(f"🔍 Financial data extracted for {asset_name}:")
        print(f"   Report Date: {report_date}")
        print(f"   Total OI: {total_oi:,}")
        print(f"   Non-Commercial Long: {non_commercial_long:,}, Short: {non_commercial_short:,}")
        print(f"   Commercial Long: {commercial_long:,}, Short: {commercial_short:,}")

        return {
            'asset_name': asset_name,
            'report_date': report_date,
            'total_open_interest': total_oi,
            'non_commercial_long': non_commercial_long,
            'non_commercial_short': non_commercial_short,
            'spreading': 0,  # Not directly available in financial format
            'commercial_long': commercial_long,
            'commercial_short': commercial_short,
            'total_long': non_commercial_long + commercial_long + nonreportable_long,
            'total_short': non_commercial_short + commercial_short + nonreportable_short,
            'nonreportable_long': nonreportable_long,
            'nonreportable_short': nonreportable_short,
            'changes': changes
        }

    def _parse_standard_data(self, asset_section: str, asset_name: str, report_date: str) -> Dict:
        """Parse standard COT data format."""
        data_lines = asset_section.split('\n')

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
            raise Exception(f"Could not find position data in {asset_name} section")

        # Parse the position numbers - more robust extraction
        clean_line = all_line.replace(',', '')
        numbers = re.findall(r'\d+', clean_line)
        numbers = [int(n) for n in numbers]

        # Extract changes line
        changes = []
        for line in data_lines:
            if 'Changes in Commitments from:' in line:
                line_idx = data_lines.index(line)
                if line_idx + 1 < len(data_lines):
                    next_line = data_lines[line_idx + 1]
                    if ':' in next_line and any(c in next_line for c in ['-', '+']):
                        clean_changes = next_line.replace(',', '')
                        change_numbers = re.findall(r'-?\d+', clean_changes)
                        if len(change_numbers) > 1:
                            changes = [int(x) for x in change_numbers[1:]]
                        break

        return {
            'asset_name': asset_name,
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
        """Analyze the data using sophisticated contrarian COT logic."""
        analysis = {
            'overall_bias': 'NEUTRAL',
            'confidence': 'LOW',
            'signals': [],
            'key_observations': [],
            'contrarian_analysis': {},
            'positioning_extremes': {},
            'smart_money_signals': [],
            'bias_explanation': ''
        }

        # Get key metrics
        nc_net = metrics['non_commercial_net']
        comm_net = metrics['commercial_net']
        nc_long_pct = metrics.get('non_commercial_long_pct', 0)
        nc_short_pct = metrics.get('non_commercial_short_pct', 0)
        total_oi = data['total_open_interest']

        # STEP 1: EXTREME POSITIONING ANALYSIS (Your Key Insight)
        extreme_threshold = 60.0  # When specs exceed 60%, market is at extreme

        analysis['positioning_extremes'] = {
            'speculative_short_pct': nc_short_pct,
            'speculative_long_pct': nc_long_pct,
            'is_extreme_short': nc_short_pct > extreme_threshold,
            'is_extreme_long': nc_long_pct > extreme_threshold,
            'extreme_level': 'HIGH' if max(nc_short_pct, nc_long_pct) > extreme_threshold else 'MODERATE' if max(nc_short_pct, nc_long_pct) > 55 else 'LOW'
        }

        # STEP 2: CONTRARIAN LOGIC (Your Core Method)
        contrarian_signals = 0
        trend_following_signals = 0

        # Extreme Short Positioning = Contrarian Bullish
        if nc_short_pct > extreme_threshold:
            contrarian_signals += 3
            analysis['signals'].append(f"🔥 EXTREME SHORT POSITIONING: Speculators {nc_short_pct:.1f}% short - CONTRARIAN BULLISH signal")
            analysis['signals'].append("📈 Crowded short trade - fuel for potential squeeze")

        # Extreme Long Positioning = Contrarian Bearish
        elif nc_long_pct > extreme_threshold:
            contrarian_signals -= 3
            analysis['signals'].append(f"🔥 EXTREME LONG POSITIONING: Speculators {nc_long_pct:.1f}% long - CONTRARIAN BEARISH signal")
            analysis['signals'].append("📉 Crowded long trade - vulnerable to selling pressure")

        # Moderate positioning - less contrarian signal
        elif nc_short_pct > 55:
            contrarian_signals += 1
            analysis['signals'].append(f"⚠️ HIGH SHORT POSITIONING: Speculators {nc_short_pct:.1f}% short - Moderate contrarian bullish")
        elif nc_long_pct > 55:
            contrarian_signals -= 1
            analysis['signals'].append(f"⚠️ HIGH LONG POSITIONING: Speculators {nc_long_pct:.1f}% long - Moderate contrarian bearish")

        # STEP 3: SMART MONEY vs DUMB MONEY ANALYSIS (Your Insight)
        # Commercials = Smart Money (hedgers, insiders)
        # Speculators = Trend followers, often wrong at extremes

        smart_money_signals = []

        # Classic contrarian setup: Specs vs Commercials positioned opposite
        if nc_net < -3000 and comm_net > 3000:  # Specs short, Commercials long
            contrarian_signals += 2
            smart_money_signals.append("💡 SMART MONEY DIVERGENCE: Commercials long while speculators short")
            analysis['signals'].append("🏦 Smart money (commercials) betting AGAINST speculative crowd - BULLISH")

        elif nc_net > 3000 and comm_net < -3000:  # Specs long, Commercials short
            contrarian_signals -= 2
            smart_money_signals.append("💡 SMART MONEY DIVERGENCE: Commercials short while speculators long")
            analysis['signals'].append("🏦 Smart money (commercials) betting AGAINST speculative crowd - BEARISH")

        # Moderate divergence
        elif (nc_net < 0 and comm_net > 0) or (nc_net > 0 and comm_net < 0):
            divergence_strength = abs(nc_net) + abs(comm_net)
            if divergence_strength > 5000:
                contrarian_signals += 1 if nc_net < 0 else -1
                smart_money_signals.append(f"⚖️ Moderate smart money divergence (strength: {divergence_strength:,})")

        analysis['smart_money_signals'] = smart_money_signals

        # STEP 4: WEEKLY CHANGES ANALYSIS (Your Step 4)
        # Look for positioning tension - when groups move in opposite directions
        weekly_changes_analysis = []

        if 'nc_long_change' in metrics and 'nc_short_change' in metrics:
            nc_long_change = metrics['nc_long_change']
            nc_short_change = metrics['nc_short_change']
            nc_net_change = metrics.get('nc_net_change', nc_long_change - nc_short_change)

            # Analyze the weekly positioning changes
            if abs(nc_long_change) > 1000 or abs(nc_short_change) > 1000:
                if nc_short_change > nc_long_change and nc_short_change > 1000:
                    weekly_changes_analysis.append(f"📊 Speculators added {nc_short_change:,} shorts vs {nc_long_change:,} longs")
                    weekly_changes_analysis.append("⚠️ Speculators doubling down on bearish bet - increases contrarian potential")
                    contrarian_signals += 1  # More shorts = more contrarian bullish

                elif nc_long_change > nc_short_change and nc_long_change > 1000:
                    weekly_changes_analysis.append(f"📊 Speculators added {nc_long_change:,} longs vs {nc_short_change:,} shorts")
                    weekly_changes_analysis.append("⚠️ Speculators doubling down on bullish bet - increases contrarian potential")
                    contrarian_signals -= 1  # More longs = more contrarian bearish

            # Check if commercials are moving opposite to speculators
            if 'commercial_long_change' in metrics:
                comm_long_change = metrics.get('commercial_long_change', 0)
                comm_short_change = metrics.get('commercial_short_change', 0)

                # Positioning tension: Specs and Commercials moving opposite ways
                if (nc_net_change < -1000 and (comm_long_change > 500 or comm_short_change < -500)):
                    weekly_changes_analysis.append("🔥 POSITIONING TENSION: Specs more bearish while commercials more bullish")
                    contrarian_signals += 1
                elif (nc_net_change > 1000 and (comm_long_change < -500 or comm_short_change > 500)):
                    weekly_changes_analysis.append("🔥 POSITIONING TENSION: Specs more bullish while commercials more bearish")
                    contrarian_signals -= 1

        analysis['weekly_changes_analysis'] = weekly_changes_analysis

        # STEP 5: CONTRARIAN BIAS DETERMINATION (Your Logic)
        # Use contrarian signals as primary factor, not simple trend following

        analysis['contrarian_analysis'] = {
            'contrarian_signals': contrarian_signals,
            'extreme_positioning': analysis['positioning_extremes']['extreme_level'],
            'smart_money_divergence': len(smart_money_signals) > 0,
            'positioning_tension': len(weekly_changes_analysis) > 0
        }

        # Determine bias using CONTRARIAN LOGIC
        if contrarian_signals >= 3:
            analysis['overall_bias'] = 'STRONGLY BULLISH (Contrarian)'
            analysis['confidence'] = 'HIGH'
            analysis['signals'].append("🎯 CONTRARIAN CONCLUSION: Extreme bearish positioning = BULLISH opportunity")

        elif contrarian_signals >= 2:
            analysis['overall_bias'] = 'BULLISH (Contrarian)'
            analysis['confidence'] = 'HIGH' if analysis['positioning_extremes']['is_extreme_short'] else 'MEDIUM'
            analysis['signals'].append("📈 CONTRARIAN CONCLUSION: Bearish positioning = BULLISH bias")

        elif contrarian_signals >= 1:
            analysis['overall_bias'] = 'MODERATELY BULLISH (Contrarian)'
            analysis['confidence'] = 'MEDIUM'

        elif contrarian_signals <= -3:
            analysis['overall_bias'] = 'STRONGLY BEARISH (Contrarian)'
            analysis['confidence'] = 'HIGH'
            analysis['signals'].append("🎯 CONTRARIAN CONCLUSION: Extreme bullish positioning = BEARISH opportunity")

        elif contrarian_signals <= -2:
            analysis['overall_bias'] = 'BEARISH (Contrarian)'
            analysis['confidence'] = 'HIGH' if analysis['positioning_extremes']['is_extreme_long'] else 'MEDIUM'
            analysis['signals'].append("📉 CONTRARIAN CONCLUSION: Bullish positioning = BEARISH bias")

        elif contrarian_signals <= -1:
            analysis['overall_bias'] = 'MODERATELY BEARISH (Contrarian)'
            analysis['confidence'] = 'MEDIUM'

        else:
            analysis['overall_bias'] = 'NEUTRAL'
            analysis['confidence'] = 'LOW'
            analysis['signals'].append("⚖️ No clear contrarian setup - positioning not at extremes")

        # Add confidence boost for extreme positioning
        if analysis['positioning_extremes']['extreme_level'] == 'HIGH':
            if analysis['confidence'] == 'MEDIUM':
                analysis['confidence'] = 'HIGH'
            analysis['signals'].append(f"🔥 EXTREME POSITIONING DETECTED: {max(nc_short_pct, nc_long_pct):.1f}% - High confidence contrarian setup")

        # STEP 6: GENERATE BIAS EXPLANATION (Simple Description)
        analysis['bias_explanation'] = self.generate_bias_explanation(
            analysis['overall_bias'],
            nc_short_pct,
            nc_long_pct,
            nc_net,
            comm_net,
            contrarian_signals,
            analysis['positioning_extremes']['extreme_level']
        )

        # Enhanced Key Observations (Your Analysis Style)
        analysis['key_observations'] = [
            f"📊 Total Open Interest: {data['total_open_interest']:,} contracts",
            f"🎯 Speculative Positioning: Long {nc_long_pct:.1f}% | Short {nc_short_pct:.1f}%",
            f"💰 Non-Commercial Net: {nc_net:,} contracts ({'Short' if nc_net < 0 else 'Long'} bias)",
            f"🏦 Commercial Net: {comm_net:,} contracts ({'Long' if comm_net > 0 else 'Short'} bias)",
            f"⚖️ Smart Money vs Crowd: {'Divergent' if (nc_net > 0 and comm_net < 0) or (nc_net < 0 and comm_net > 0) else 'Aligned'}",
            f"🔥 Extreme Level: {analysis['positioning_extremes']['extreme_level']} ({max(nc_short_pct, nc_long_pct):.1f}% max positioning)",
            f"📈 Contrarian Signal Strength: {contrarian_signals} ({'Bullish' if contrarian_signals > 0 else 'Bearish' if contrarian_signals < 0 else 'Neutral'})"
        ]

        # Add weekly changes to observations if available
        if weekly_changes_analysis:
            analysis['key_observations'].extend([
                "📊 Weekly Changes Analysis:",
                *[f"   • {obs}" for obs in weekly_changes_analysis[:2]]  # Top 2 changes
            ])

        # Add smart money signals to observations
        if smart_money_signals:
            analysis['key_observations'].extend([
                "🏦 Smart Money Signals:",
                *[f"   • {signal}" for signal in smart_money_signals[:2]]  # Top 2 signals
            ])

        return analysis

    def generate_bias_explanation(self, bias: str, nc_short_pct: float, nc_long_pct: float,
                                 nc_net: int, comm_net: int, contrarian_signals: int, extreme_level: str) -> str:
        """Generate a simple, clear explanation of why the bias was determined."""

        # Determine the main positioning scenario
        is_extreme_short = nc_short_pct > 60
        is_extreme_long = nc_long_pct > 60
        is_moderate_short = nc_short_pct > 55
        is_moderate_long = nc_long_pct > 55

        # Smart money divergence
        smart_money_opposite = (nc_net > 0 and comm_net < 0) or (nc_net < 0 and comm_net > 0)

        explanation = ""

        if 'BULLISH' in bias:
            if is_extreme_short:
                explanation = f"""🎯 Why BULLISH (Contrarian Setup):

The Crowd is Extremely Bearish - Speculators are {nc_short_pct:.1f}% short, which is an extreme level (over 60%).

Contrarian Logic: When everyone is betting one way, the market often moves the opposite direction. Here's why:

• Crowded Trade: With {nc_short_pct:.1f}% of speculators short, there are very few sellers left
• Short Squeeze Potential: All these shorts will eventually need to buy back (cover), creating buying pressure
• Smart Money: Commercials (the insiders/hedgers) are positioned {('long' if comm_net > 0 else 'short')}, often opposite to the crowd at turning points

Historical Pattern: When speculative shorts exceed 60%, the market typically rebounds as shorts are forced to cover their positions.

Bottom Line: Too many people are betting against this asset - that's usually when it surprises everyone and goes up instead."""

            elif is_moderate_short:
                explanation = f"""📈 Why BULLISH (Contrarian Setup):

Speculators are Heavily Short - {nc_short_pct:.1f}% of speculators are betting against this asset.

The Setup: This creates a contrarian opportunity because:

• Imbalanced Positioning: More people are short than long, creating potential for a squeeze
• Smart Money Divergence: {('Commercials are positioned opposite to speculators' if smart_money_opposite else 'Positioning shows potential for reversal')}
• Covering Pressure: Short positions will need to be bought back, providing upward pressure

Why This Matters: Markets often move against the crowd, especially when positioning becomes one-sided."""

        elif 'BEARISH' in bias:
            if is_extreme_long:
                explanation = f"""🎯 Why BEARISH (Contrarian Setup):

The Crowd is Extremely Bullish - Speculators are {nc_long_pct:.1f}% long, which is an extreme level (over 60%).

Contrarian Logic: When everyone is betting one way, the market often moves the opposite direction. Here's why:

• Crowded Trade: With {nc_long_pct:.1f}% of speculators long, there are very few buyers left
• Selling Pressure: All these longs are vulnerable to selling if the market turns
• Smart Money: Commercials (the insiders/hedgers) are positioned {('short' if comm_net < 0 else 'long')}, often opposite to the crowd

Historical Pattern: When speculative longs exceed 60%, the market typically declines as longs get shaken out.

Bottom Line: Too many people are betting on this asset going up - that's usually when it disappoints and goes down instead."""

            elif is_moderate_long:
                explanation = f"""📉 Why BEARISH (Contrarian Setup):

Speculators are Heavily Long - {nc_long_pct:.1f}% of speculators are betting on this asset rising.

The Setup: This creates a contrarian opportunity because:

• Imbalanced Positioning: More people are long than short, creating vulnerability
• Smart Money Divergence: {('Commercials are positioned opposite to speculators' if smart_money_opposite else 'Positioning shows potential for reversal')}
• Selling Pressure: Long positions are vulnerable to profit-taking and stops

Why This Matters: Markets often move against the crowd, especially when positioning becomes one-sided."""

        else:  # NEUTRAL
            explanation = f"""⚖️ Why NEUTRAL:

Balanced Positioning - Speculators are {nc_long_pct:.1f}% long and {nc_short_pct:.1f}% short.

The Setup: No clear contrarian opportunity because:

• No Extreme Positioning: Neither longs nor shorts are at extreme levels (60%+)
• Limited Contrarian Signals: {contrarian_signals} contrarian signals detected
• Wait for Setup: Best to wait for clearer positioning extremes

Strategy: Monitor for positioning to reach extreme levels (60%+) before taking contrarian positions."""

        return explanation

    def run_analysis(self, asset_name: str = 'USD INDEX') -> Dict:
        """Run the complete COT analysis for specified asset."""
        print(f"🔄 Fetching latest {asset_name} COT data...")

        if asset_name not in self.available_assets:
            raise Exception(f"Asset '{asset_name}' not supported")

        source = self.available_assets[asset_name]['source']
        html_content = self.fetch_cot_data(source)

        print(f"📊 Parsing {asset_name} data...")
        self.data = self.parse_asset_data(html_content, asset_name)

        # Debug: Print the extracted date
        print(f"📅 Extracted report date: {self.data.get('report_date', 'Unknown')}")

        print("🧮 Calculating metrics...")
        metrics = self.calculate_metrics(self.data)

        print("🎯 Analyzing directional bias...")
        self.analysis_results = self.analyze_directional_bias(self.data, metrics)

        return {
            'data': self.data,
            'metrics': metrics,
            'analysis': self.analysis_results
        }

def main():
    """Main execution function."""
    try:
        analyzer = MultiAssetCOTAnalyzer()

        # Show available assets
        assets = analyzer.get_available_assets()
        print("Available assets for analysis:")
        for asset in assets:
            print(f"  - {asset['name']}: {asset['description']}")

        # Default analysis for USD INDEX
        results = analyzer.run_analysis('USD INDEX')

        # Print basic results
        print(f"\n🎯 Analysis Results for {results['data']['asset_name']}:")
        print(f"Overall Bias: {results['analysis']['overall_bias']}")
        print(f"Confidence: {results['analysis']['confidence']}")
        print(f"Report Date: {results['data']['report_date']}")

        return results

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return None

if __name__ == "__main__":
    main()
