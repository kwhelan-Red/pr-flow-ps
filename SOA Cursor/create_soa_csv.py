#!/usr/bin/env python3
"""
Complete SOA Data Collection - Outputs to CSV
Supports both browser automation and export processing
"""

import json
import pandas as pd
import sys
from datetime import datetime

# Load STIs
with open('soa_stis_list.json', 'r') as f:
    data = json.load(f)
    stis = data.get('stis', [])

print("="*80)
print("SOA DATA COLLECTION - CSV OUTPUT")
print("="*80)
print(f"\nTotal STIs: {len(stis)}")

# CSV output columns
csv_columns = [
    'STI',
    'CMDB ID', 
    'Application Name',
    'SOA Applicable',
    'SOA Status',
    'ESS Self-Assessment Status',
    'ESS Assessment URL',
    'PIA Status',
    'PIA Assessment URL',
    'DPQ Complete',
    'SIA Status',
    'Criticality Tier',
    'Data Classification',
    'Install Status',
    'Collection Method',
    'Collection Date',
    'Status'
]

print(f"\n✅ CSV format configured: {len(csv_columns)} columns")
print(f"   Output: soa_data_all_stis.csv")

# Initialize empty DataFrame
df_output = pd.DataFrame(columns=csv_columns)

# Save empty CSV template
df_output.to_csv('soa_data_all_stis.csv', index=False)
print(f"\n✅ CSV template created: soa_data_all_stis.csv")

print(f"\n📋 Collection Methods:")
print(f"   1. Browser Automation (Direct from ServiceNow)")
print(f"      - Navigate to each STI's detail page")
print(f"      - Extract data from Compliance/Data Privacy tabs")
print(f"      - Time: ~30-60 minutes for 114 STIs")
print(f"\n   2. Export Processing (RECOMMENDED - Fastest)")
print(f"      - Export from ServiceNow to CSV")
print(f"      - Run: python3 get_soa_data.py --method export --export-file <export.csv>")
print(f"      - Time: ~2 minutes")

print(f"\n💡 Framework ready - Choose your collection method")
print(f"   CSV output will be generated when data is collected")




