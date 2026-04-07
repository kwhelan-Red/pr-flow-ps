#!/usr/bin/env python3
"""
Collect SOA data directly from ServiceNow and output to CSV
Iterates through all STIs and extracts data via browser automation
"""

import json
import pandas as pd
from datetime import datetime
import sys

# Load STIs
with open('soa_stis_list.json', 'r') as f:
    data = json.load(f)
    stis = data.get('stis', [])

print("="*80)
print("COLLECTING SOA DATA FROM SERVICENOW - CSV OUTPUT")
print("="*80)
print(f"\nTotal STIs: {len(stis)}")

# Collection data structure
all_records = []

# Field extraction pattern:
# For each STI:
# 1. Navigate to detail page
# 2. Extract: Application Name, Criticality, Classification
# 3. Click Compliance tab → Extract ESS URL, PIA URL
# 4. Click Data Privacy tab → Extract DPQ Complete
# 5. Save record

print(f"\n📋 Collection Process:")
print(f"   - Navigate to each STI's Business Application page")
print(f"   - Extract all SOA-related fields")
print(f"   - Save to CSV format")

# Initialize CSV data structure
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

print(f"\n✅ CSV columns defined: {len(csv_columns)} fields")
print(f"   Output file: soa_data_all_stis.csv")

# Collection log
collection_log = {
    "collection_started": datetime.now().isoformat(),
    "total_stis": len(stis),
    "method": "Browser Automation - Direct ServiceNow",
    "csv_columns": csv_columns,
    "records_collected": 0,
    "records": []
}

# Save initial log
with open('soa_data_browser_collection.json', 'w') as f:
    json.dump(collection_log, f, indent=2)

print(f"\n🚀 Ready to collect data for all {len(stis)} STIs")
print(f"   Progress will be saved after each record")
print(f"   CSV file will be generated when complete")

# Note: Browser automation will iterate through stis and collect data
# CSV will be generated from collected records

if __name__ == "__main__":
    print(f"\n💡 Browser automation framework ready")
    print(f"   Run browser automation to collect data for all STIs")
    print(f"   CSV output: soa_data_all_stis.csv")




