#!/usr/bin/env python3
"""
Example usage of the USD Index COT Analyzer
Demonstrates different ways to use the analyzer programmatically
"""

from usd_index_cot_analyzer import USDIndexCOTAnalyzer
import json

def basic_analysis():
    """Basic analysis example"""
    print("=" * 50)
    print("BASIC ANALYSIS EXAMPLE")
    print("=" * 50)
    
    # Create analyzer and run analysis
    analyzer = USDIndexCOTAnalyzer()
    results = analyzer.run_analysis()
    
    # Print the formatted report
    analyzer.print_report()
    
    return results

def detailed_data_access():
    """Example of accessing detailed data"""
    print("\n" + "=" * 50)
    print("DETAILED DATA ACCESS EXAMPLE")
    print("=" * 50)
    
    analyzer = USDIndexCOTAnalyzer()
    results = analyzer.run_analysis()
    
    # Access individual components
    data = results['data']
    metrics = results['metrics']
    analysis = results['analysis']
    
    print(f"\n📊 RAW DATA:")
    print(f"Report Date: {data['report_date']}")
    print(f"Total Open Interest: {data['total_open_interest']:,}")
    print(f"Non-Commercial Long: {data['non_commercial_long']:,}")
    print(f"Non-Commercial Short: {data['non_commercial_short']:,}")
    print(f"Commercial Long: {data['commercial_long']:,}")
    print(f"Commercial Short: {data['commercial_short']:,}")
    
    print(f"\n🧮 CALCULATED METRICS:")
    print(f"Non-Commercial Net: {metrics['non_commercial_net']:,}")
    print(f"Commercial Net: {metrics['commercial_net']:,}")
    print(f"NC Long %: {metrics.get('non_commercial_long_pct', 0):.1f}%")
    print(f"NC Short %: {metrics.get('non_commercial_short_pct', 0):.1f}%")
    
    print(f"\n🎯 ANALYSIS RESULTS:")
    print(f"Overall Bias: {analysis['overall_bias']}")
    print(f"Confidence: {analysis['confidence']}")
    print(f"Number of Signals: {len(analysis['signals'])}")
    
    return results

def custom_analysis_logic():
    """Example of implementing custom analysis logic"""
    print("\n" + "=" * 50)
    print("CUSTOM ANALYSIS LOGIC EXAMPLE")
    print("=" * 50)
    
    analyzer = USDIndexCOTAnalyzer()
    results = analyzer.run_analysis()
    
    data = results['data']
    metrics = results['metrics']
    
    # Custom analysis logic
    print(f"\n🔍 CUSTOM ANALYSIS:")
    
    # Calculate custom ratios
    total_positions = data['non_commercial_long'] + data['non_commercial_short']
    long_dominance = (data['non_commercial_long'] / total_positions) * 100 if total_positions > 0 else 0
    
    print(f"Speculative Long Dominance: {long_dominance:.1f}%")
    
    # Custom sentiment score
    sentiment_score = 0
    
    # Add points for bullish factors
    if metrics['non_commercial_net'] > 0:
        sentiment_score += 2
    if metrics.get('non_commercial_long_pct', 0) > 45:
        sentiment_score += 1
    if metrics.get('nc_net_change', 0) > 500:
        sentiment_score += 1
    
    # Subtract points for bearish factors
    if metrics['non_commercial_net'] < 0:
        sentiment_score -= 2
    if metrics.get('non_commercial_short_pct', 0) > 45:
        sentiment_score -= 1
    if metrics.get('nc_net_change', 0) < -500:
        sentiment_score -= 1
    
    print(f"Custom Sentiment Score: {sentiment_score}")
    
    if sentiment_score >= 2:
        custom_bias = "BULLISH"
    elif sentiment_score <= -2:
        custom_bias = "BEARISH"
    else:
        custom_bias = "NEUTRAL"
    
    print(f"Custom Bias: {custom_bias}")
    
    return results

def export_data_example():
    """Example of exporting data to different formats"""
    print("\n" + "=" * 50)
    print("DATA EXPORT EXAMPLE")
    print("=" * 50)
    
    analyzer = USDIndexCOTAnalyzer()
    results = analyzer.run_analysis()
    
    # Export to JSON
    with open('cot_analysis_results.json', 'w') as f:
        # Convert numpy types to native Python types for JSON serialization
        json_results = {}
        for key, value in results.items():
            if isinstance(value, dict):
                json_results[key] = {k: int(v) if isinstance(v, (int, float)) else v 
                                   for k, v in value.items()}
            else:
                json_results[key] = value
        
        json.dump(json_results, f, indent=2)
    
    print("✅ Results exported to 'cot_analysis_results.json'")
    
    # Create a simple CSV-like summary
    with open('cot_summary.txt', 'w') as f:
        f.write("USD Index COT Analysis Summary\n")
        f.write("=" * 40 + "\n")
        f.write(f"Date: {results['data']['report_date']}\n")
        f.write(f"Overall Bias: {results['analysis']['overall_bias']}\n")
        f.write(f"Confidence: {results['analysis']['confidence']}\n")
        f.write(f"Open Interest: {results['data']['total_open_interest']}\n")
        f.write(f"NC Net Position: {results['metrics']['non_commercial_net']}\n")
        f.write(f"Commercial Net: {results['metrics']['commercial_net']}\n")
        f.write("\nSignals:\n")
        for i, signal in enumerate(results['analysis']['signals'], 1):
            f.write(f"{i}. {signal}\n")
    
    print("✅ Summary exported to 'cot_summary.txt'")
    
    return results

def main():
    """Run all examples"""
    try:
        # Run basic analysis
        basic_analysis()
        
        # Show detailed data access
        detailed_data_access()
        
        # Demonstrate custom analysis
        custom_analysis_logic()
        
        # Export data examples
        export_data_example()
        
        print("\n" + "=" * 50)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")

if __name__ == "__main__":
    main()
