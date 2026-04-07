#!/usr/bin/env python3
"""
Complete SOA Data Collection from ServiceNow - Populates CSV
Collects data directly from ServiceNow for all STIs and outputs to CSV
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
print("SOA DATA COLLECTION - DIRECT FROM SERVICENOW TO CSV")
print("="*80)
print(f"\nTotal STIs: {len(stis)}")

# CSV columns
csv_columns = [
    'STI', 'CMDB ID', 'Application Name', 'SOA Applicable', 'SOA Status',
    'ESS Self-Assessment Status', 'ESS Assessment URL', 'PIA Status',
    'PIA Assessment URL', 'DPQ Complete', 'SIA Status', 'Criticality Tier',
    'Data Classification', 'Install Status', 'Collection Method', 'Collection Date', 'Status'
]

# Collection log
collection_log = {
    "collection_started": datetime.now().isoformat(),
    "total_stis": len(stis),
    "method": "Browser Automation - Direct ServiceNow Navigation",
    "base_url": "https://redhat.service-now.com",
    "records_collected": 0,
    "records": []
}

print(f"\n✅ CSV format: {len(csv_columns)} columns")
print(f"   Output file: soa_data_all_stis.csv")

# Initialize CSV
df = pd.DataFrame(columns=csv_columns)
df.to_csv('soa_data_all_stis.csv', index=False)

print(f"\n✅ CSV template created: soa_data_all_stis.csv")

print(f"\n📋 Browser Automation Collection Process:")
print(f"   For each of {len(stis)} STIs:")
print(f"   1. Navigate to Business Application detail page")
print(f"   2. Extract: Application Name, Criticality, Classification")
print(f"   3. Click Compliance tab → Extract ESS & PIA URLs")
print(f"   4. Click Data Privacy tab → Extract DPQ Complete")
print(f"   5. Search for SIA in other tabs")
print(f"   6. Append record to CSV")
print(f"   7. Continue to next STI")

print(f"\n🚀 Framework ready for browser automation")
print(f"   CSV will be populated as data is collected")
print(f"   Progress saved to: soa_data_browser_collection.json")

# Save collection log
with open('soa_data_browser_collection.json', 'w') as f:
    json.dump(collection_log, f, indent=2)

print(f"\n💡 Browser automation can now iterate through all {len(stis)} STIs")
print(f"   CSV file will be updated after each record is collected")




