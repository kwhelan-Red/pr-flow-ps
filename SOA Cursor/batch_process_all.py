#!/usr/bin/env python3
"""
Batch process all STIs from JSON data
Processes multiple STIs at once from a JSON file or directory
"""

import json
import pandas as pd
import sys
import argparse
import os
from datetime import datetime
from process_console_output import parse_console_output, update_csv_with_results

def load_stis():
    """Load all STIs from CSV"""
    try:
        df = pd.read_csv('soa_data_all_stis.csv')
        return df['STI'].tolist()
    except FileNotFoundError:
        print("❌ Error: soa_data_all_stis.csv not found")
        sys.exit(1)

def process_all_from_json_file(json_file):
    """Process all STIs from a single JSON file containing multiple STIs"""
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {json_file}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {json_file}: {e}")
        return
    
    # Check if it's a list of STI data or a dict with STI keys
    if isinstance(data, list):
        # List format: [{"sti": "AAP-001", "data": {...}}, ...]
        for item in data:
            sti = item.get('sti') or item.get('STI')
            sti_data = item.get('data') or item
            if sti:
                print(f"\nProcessing {sti}...")
                update_csv_with_results('soa_data_all_stis.csv', sti, sti_data)
    elif isinstance(data, dict):
        # Dict format: {"AAP-001": {...}, "ANSI-001": {...}}
        for sti, sti_data in data.items():
            if sti.upper() != 'STI' and sti.upper() != 'CMDB ID':  # Skip header-like keys
                print(f"\nProcessing {sti}...")
                update_csv_with_results('soa_data_all_stis.csv', sti, sti_data)

def process_all_from_directory(directory):
    """Process all JSON files in a directory (one STI per file)"""
    if not os.path.exists(directory):
        print(f"❌ Error: Directory not found: {directory}")
        return
    
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]
    
    if not json_files:
        print(f"⚠️  No JSON files found in {directory}")
        return
    
    print(f"📁 Found {len(json_files)} JSON files")
    
    processed = 0
    failed = 0
    
    for json_file in json_files:
        # Extract STI from filename (e.g., AAP-001.json)
        sti = os.path.splitext(json_file)[0]
        file_path = os.path.join(directory, json_file)
        
        print(f"\nProcessing {sti}...")
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            results = parse_console_output(content)
            if results:
                if update_csv_with_results('soa_data_all_stis.csv', sti, results):
                    processed += 1
                else:
                    failed += 1
            else:
                print(f"  ❌ Could not parse JSON")
                failed += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1
    
    print(f"\n{'='*80}")
    print(f"BATCH PROCESSING COMPLETE")
    print(f"{'='*80}")
    print(f"✅ Processed: {processed}")
    print(f"❌ Failed: {failed}")

def create_template_json():
    """Create a template JSON file for batch processing"""
    stis = load_stis()
    
    template = {
        "instructions": "Fill in JSON data for each STI",
        "format": "Each STI should have: applicationName, criticalityTier, essUrl, piaUrl, dpqComplete",
        "stis": {}
    }
    
    for sti in stis[:5]:  # Show first 5 as examples
        template["stis"][sti] = {
            "applicationName": "empty value",
            "criticalityTier": "empty value",
            "essUrl": "empty value",
            "piaUrl": "empty value",
            "dpqComplete": "empty value"
        }
    
    with open('batch_template.json', 'w') as f:
        json.dump(template, f, indent=2)
    
    print("✅ Created batch_template.json")
    print(f"   Template shows format for {len(stis)} STIs")
    print(f"   Fill in data and run: python3 batch_process_all.py --file batch_template.json")

def main():
    parser = argparse.ArgumentParser(description="Batch process all STIs")
    parser.add_argument("--file", help="JSON file with all STI data")
    parser.add_argument("--dir", help="Directory with JSON files (one per STI)")
    parser.add_argument("--template", action='store_true', help="Create template JSON file")
    parser.add_argument("--csv", default="soa_data_all_stis.csv", help="CSV file to update")
    
    args = parser.parse_args()
    
    print("="*80)
    print("BATCH PROCESS ALL STIs")
    print("="*80)
    
    if args.template:
        create_template_json()
        return
    
    if args.file:
        print(f"\n📁 Processing from file: {args.file}")
        process_all_from_json_file(args.file)
    elif args.dir:
        print(f"\n📁 Processing from directory: {args.dir}")
        process_all_from_directory(args.dir)
    else:
        print("\n❌ Error: Need --file or --dir")
        print("\nUsage:")
        print("  python3 batch_process_all.py --file all_stis_data.json")
        print("  python3 batch_process_all.py --dir console_outputs/")
        print("  python3 batch_process_all.py --template  # Create template")
        sys.exit(1)
    
    # Show final status
    print(f"\n📊 Final Status:")
    os.system("python3 check_extraction_status.py")

if __name__ == "__main__":
    main()




