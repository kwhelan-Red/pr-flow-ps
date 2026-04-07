#!/usr/bin/env python3
"""
Process manual console output from JavaScript extraction
Reads JSON from console output and updates CSV
"""

import pandas as pd
import json
import sys
import argparse
from datetime import datetime
import re

def parse_console_output(console_output):
    """Parse JSON from console output"""
    # Try to find JSON in the output
    # Look for patterns like: {"applicationName": ..., "criticalityTier": ...}
    json_pattern = r'\{[^{}]*"applicationName"[^{}]*\{[^{}]*\}[^{}]*\}|\{[^{}]*"applicationName"[^{}]*\}'
    
    # Try direct JSON parsing first
    try:
        # Remove any leading/trailing whitespace
        cleaned = console_output.strip()
        # Try to parse as JSON
        data = json.loads(cleaned)
        return data
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from console.log output
    # Pattern: console.log('Extracted:', JSON.stringify(...))
    match = re.search(r'JSON\.stringify\(([^)]+)\)', console_output)
    if match:
        try:
            data = json.loads(match.group(1))
            return data
        except:
            pass
    
    # Try to find JSON object in output
    json_match = re.search(r'\{[^{}]*(?:"applicationName"|"criticalityTier"|"essUrl"|"piaUrl"|"dpqComplete")[^{}]*\}', console_output, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group(0))
            return data
        except:
            pass
    
    # Try to find JSON between braces
    brace_start = console_output.find('{')
    brace_end = console_output.rfind('}')
    if brace_start != -1 and brace_end != -1 and brace_end > brace_start:
        json_str = console_output[brace_start:brace_end+1]
        try:
            data = json.loads(json_str)
            return data
        except:
            pass
    
    return None

def update_csv_with_results(csv_file, sti, results):
    """Update CSV with extracted results"""
    df = pd.read_csv(csv_file)
    
    # Find row for this STI
    if sti not in df['STI'].values:
        print(f"⚠️  Warning: STI {sti} not found in CSV")
        return False
    
    idx = df[df['STI'] == sti].index[0]
    
    # Map results to CSV columns
    column_mapping = {
        'applicationName': 'Application Name',
        'criticalityTier': 'Criticality Tier',
        'essUrl': 'ESS Assessment URL',
        'piaUrl': 'PIA Assessment URL',
        'dpqComplete': 'DPQ Complete'
    }
    
    updated_fields = []
    for js_key, csv_col in column_mapping.items():
        if js_key in results:
            value = results[js_key]
            # Ensure empty values are marked as "empty value"
            if not value or value.strip() == '' or value == '-- None --':
                value = 'empty value'
            df.at[idx, csv_col] = value
            updated_fields.append(csv_col)
    
    # Update status
    df.at[idx, 'Status'] = 'Extracted via Console'
    df.at[idx, 'Collection Date'] = datetime.now().isoformat()
    
    # Save CSV
    df.to_csv(csv_file, index=False)
    
    print(f"✅ Updated {sti}: {len(updated_fields)} fields")
    for field in updated_fields:
        value = df.at[idx, field]
        print(f"   {field}: {value}")
    
    return True

def process_from_file(input_file, csv_file, sti):
    """Process JSON from file"""
    try:
        with open(input_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {input_file}")
        return False
    
    results = parse_console_output(content)
    if not results:
        print(f"❌ Error: Could not parse JSON from {input_file}")
        print(f"   Content preview: {content[:200]}")
        return False
    
    return update_csv_with_results(csv_file, sti, results)

def process_from_stdin(csv_file, sti):
    """Process JSON from stdin"""
    print(f"📋 Paste console output (JSON) and press Ctrl+D (Mac/Linux) or Ctrl+Z (Windows):")
    content = sys.stdin.read()
    
    results = parse_console_output(content)
    if not results:
        print(f"❌ Error: Could not parse JSON from input")
        print(f"   Content preview: {content[:200]}")
        return False
    
    return update_csv_with_results(csv_file, sti, results)

def main():
    parser = argparse.ArgumentParser(description="Process manual console output and update CSV")
    parser.add_argument("--csv", default="soa_data_all_stis.csv", help="CSV file to update")
    parser.add_argument("--sti", required=True, help="STI identifier (e.g., ATRO-001)")
    parser.add_argument("--file", help="File containing console output (JSON)")
    parser.add_argument("--json", help="Direct JSON string")
    
    args = parser.parse_args()
    
    print("="*80)
    print("PROCESSING MANUAL CONSOLE OUTPUT")
    print("="*80)
    print(f"\n📊 CSV File: {args.csv}")
    print(f"📋 STI: {args.sti}\n")
    
    if args.json:
        results = parse_console_output(args.json)
        if results:
            update_csv_with_results(args.csv, args.sti, results)
        else:
            print("❌ Error: Could not parse JSON")
    elif args.file:
        process_from_file(args.file, args.csv, args.sti)
    else:
        process_from_stdin(args.csv, args.sti)

if __name__ == "__main__":
    main()




