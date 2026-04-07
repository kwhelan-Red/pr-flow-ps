#!/usr/bin/env python3
"""
Batch processor for multiple console outputs
Processes multiple JSON files at once
"""

import json
import pandas as pd
import sys
import argparse
import os
from glob import glob
from process_console_output import parse_console_output, update_csv_with_results

def process_batch(input_dir, csv_file):
    """Process all JSON files in directory"""
    json_files = glob(os.path.join(input_dir, "*.json"))
    
    if not json_files:
        print(f"⚠️  No JSON files found in {input_dir}")
        return
    
    print("="*80)
    print("BATCH PROCESSING CONSOLE OUTPUTS")
    print("="*80)
    print(f"\n📁 Input Directory: {input_dir}")
    print(f"📊 CSV File: {csv_file}")
    print(f"📋 Found {len(json_files)} JSON files\n")
    
    processed = 0
    failed = 0
    
    for json_file in json_files:
        # Extract STI from filename (e.g., ATRO-001.json)
        filename = os.path.basename(json_file)
        sti = os.path.splitext(filename)[0]
        
        print(f"Processing: {sti}...")
        
        try:
            with open(json_file, 'r') as f:
                content = f.read()
            
            results = parse_console_output(content)
            if results:
                if update_csv_with_results(csv_file, sti, results):
                    processed += 1
                else:
                    failed += 1
            else:
                print(f"  ❌ Could not parse JSON")
                failed += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1
    
    print(f"\n✅ Batch processing complete:")
    print(f"   Processed: {processed}")
    print(f"   Failed: {failed}")

def main():
    parser = argparse.ArgumentParser(description="Batch process console outputs")
    parser.add_argument("--input-dir", default="console_outputs", help="Directory containing JSON files")
    parser.add_argument("--csv", default="soa_data_all_stis.csv", help="CSV file to update")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_dir):
        print(f"❌ Error: Directory not found: {args.input_dir}")
        sys.exit(1)
    
    process_batch(args.input_dir, args.csv)

if __name__ == "__main__":
    main()




