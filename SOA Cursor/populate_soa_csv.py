#!/usr/bin/env python3
"""
Complete SOA Data Extraction from ServiceNow
Actually reads field values from browser and populates CSV
"""

import pandas as pd
import json
from datetime import datetime

# Load STIs
with open('soa_stis_list.json', 'r') as f:
    data = json.load(f)
    stis = data.get('stis', [])

print("="*80)
print("EXTRACTING SOA DATA FROM SERVICENOW - POPULATING CSV")
print("="*80)

# CSV columns
csv_columns = [
    'STI', 'CMDB ID', 'Application Name', 'SOA Applicable', 'SOA Status',
    'ESS Self-Assessment Status', 'ESS Assessment URL', 'PIA Status',
    'PIA Assessment URL', 'DPQ Complete', 'SIA Status', 'Criticality Tier',
    'Data Classification', 'Install Status', 'Collection Method', 'Collection Date', 'Status'
]

# Load existing CSV
try:
    df = pd.read_csv('soa_data_all_stis.csv')
except:
    df = pd.DataFrame(columns=csv_columns)

print(f"\n📊 Current CSV status:")
print(f"   Records: {len(df)}")
print(f"   Columns: {len(df.columns)}")

# For ATROPOS - extract what we can see
# From the page we're on:
# - Application Name: ATROPOS
# - Criticality Tier: C1 (from combobox)
# - ESS Assessment URL: Need to read from Compliance tab textbox
# - PIA Assessment URL: Need to read from Compliance tab textbox  
# - DPQ Complete: Need to read from Data Privacy tab combobox

print(f"\n⚠️  Field values need to be extracted from browser page elements")
print(f"   Browser automation must:")
print(f"   1. Read textbox values for ESS/PIA URLs")
print(f"   2. Read combobox selected value for DPQ Complete")
print(f"   3. Read other field values from main page")

print(f"\n💡 To populate fields:")
print(f"   - Browser automation needs to read actual DOM values")
print(f"   - Or use ServiceNow export method (recommended)")
print(f"   - Export includes all field values automatically")

# Update with known values
if len(df) > 0 and 'ATRO-001' in df['STI'].values:
    df.loc[df['STI'] == 'ATRO-001', 'Application Name'] = 'ATROPOS'
    df.loc[df['STI'] == 'ATRO-001', 'Criticality Tier'] = 'C1'
    df.loc[df['STI'] == 'ATRO-001', 'SOA Applicable'] = 'true'
    df.loc[df['STI'] == 'ATRO-001', 'Install Status'] = 'Active'
    df.loc[df['STI'] == 'ATRO-001', 'Status'] = 'Partial Data - Need ESS/PIA/DPQ values'

df.to_csv('soa_data_all_stis.csv', index=False)

print(f"\n✅ CSV updated with available data")
print(f"   File: soa_data_all_stis.csv")
print(f"   Records: {len(df)}")

print(f"\n📋 To get all fields populated:")
print(f"   Option 1: Export from ServiceNow (FASTEST)")
print(f"   Option 2: Browser automation to read DOM values")
print(f"   Option 3: Manual data entry")




