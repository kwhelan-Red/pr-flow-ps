#!/usr/bin/env python3
"""
Simple helper script to show available STIs and test the process
"""

import pandas as pd
import json
import sys

print("="*80)
print("SOA EXTRACTION HELPER")
print("="*80)

try:
    df = pd.read_csv('soa_data_all_stis.csv')
except FileNotFoundError:
    print("❌ Error: soa_data_all_stis.csv not found")
    print("   Make sure you're in the right folder:")
    print("   cd '/Users/kwhelan/pr-flow-ps/SOA Cursor'")
    sys.exit(1)

print(f"\n📊 Total STIs in CSV: {len(df)}")
print(f"\n📋 First 10 STIs (use any of these):")
for i, sti in enumerate(df['STI'].head(10), 1):
    print(f"   {i}. {sti}")

print(f"\n💡 To extract data for a specific STI:")
print(f"   1. Get JSON from browser console (see QUICK_START.md)")
print(f"   2. Run this command:")
print(f"      python3 process_console_output.py --sti <STI_NAME> --json '<YOUR_JSON>'")
print(f"\n   Example:")
first_sti = df['STI'].iloc[0]
sample_json = {
    "applicationName": "Example App",
    "criticalityTier": "C1",
    "essUrl": "empty value",
    "piaUrl": "empty value",
    "dpqComplete": "empty value"
}
print(f"      python3 process_console_output.py --sti {first_sti} --json '{json.dumps(sample_json)}'")

print(f"\n📖 For detailed instructions:")
print(f"   python3 how_to_run.py")
print(f"   cat QUICK_START.md")




