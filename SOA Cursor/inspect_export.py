#!/usr/bin/env python3
"""
Debug script to inspect ServiceNow export columns and data
Helps identify which columns contain SOA-related data
"""

import pandas as pd
import sys
import argparse

def inspect_servicenow_export(csv_file):
    """Inspect ServiceNow export to identify columns and sample data"""
    
    print(f"📊 Inspecting ServiceNow export: {csv_file}")
    print("="*80)
    
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return
    
    print(f"\n✅ Loaded {len(df)} records")
    print(f"📋 Total columns: {len(df.columns)}\n")
    
    # Show all columns
    print("ALL COLUMNS:")
    print("-"*80)
    for i, col in enumerate(df.columns, 1):
        print(f"{i:3d}. {col}")
    
    # Identify potential SOA-related columns
    print("\n\nPOTENTIAL SOA-RELATED COLUMNS:")
    print("-"*80)
    
    soa_keywords = ['soa', 'ess', 'pia', 'sia', 'privacy', 'security', 'assessment', 
                   'criticality', 'classification', 'status', 'applicable', 'dpq']
    
    relevant_cols = {}
    for keyword in soa_keywords:
        matching = [col for col in df.columns if keyword in str(col).lower()]
        if matching:
            relevant_cols[keyword] = matching
    
    for keyword, cols in relevant_cols.items():
        print(f"\n{keyword.upper()}:")
        for col in cols:
            # Show sample values
            sample_vals = df[col].dropna().head(3).tolist()
            print(f"  - {col}")
            if sample_vals:
                print(f"    Sample values: {sample_vals}")
    
    # Show sample row
    print("\n\nSAMPLE ROW (first record):")
    print("-"*80)
    if len(df) > 0:
        sample_row = df.iloc[0]
        for col in df.columns:
            val = sample_row[col]
            if pd.notna(val) and str(val).strip():
                val_str = str(val)[:100]  # Truncate long values
                print(f"{col}: {val_str}")
    
    # Check for Application ID column
    print("\n\nAPPLICATION ID COLUMN SEARCH:")
    print("-"*80)
    app_id_candidates = [col for col in df.columns if 'id' in str(col).lower() or 'application' in str(col).lower()]
    for col in app_id_candidates:
        print(f"  - {col}")
        if len(df) > 0:
            sample_vals = df[col].dropna().head(5).tolist()
            print(f"    Sample values: {sample_vals}")

def main():
    parser = argparse.ArgumentParser(description="Inspect ServiceNow export to identify columns")
    parser.add_argument("csv_file", help="ServiceNow CSV export file")
    args = parser.parse_args()
    
    inspect_servicenow_export(args.csv_file)

if __name__ == "__main__":
    main()




