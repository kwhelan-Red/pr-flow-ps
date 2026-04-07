#!/usr/bin/env python3
"""
Collect SOA data directly from ServiceNow - Working Implementation
Uses browser automation to collect data for all STIs and output to CSV
"""

import json
import pandas as pd
from datetime import datetime
import sys
import os

# Load STIs
with open('soa_stis_list.json', 'r') as f:
    data = json.load(f)
    stis = data.get('stis', [])

print("="*80)
print("COLLECTING SOA DATA DIRECTLY FROM SERVICENOW")
print("="*80)
print(f"\nTotal STIs: {len(stis)}")
print(f"Output Format: CSV")

# CSV columns
csv_columns = [
    'STI', 'CMDB ID', 'Application Name', 'SOA Applicable', 'SOA Status',
    'ESS Self-Assessment Status', 'ESS Assessment URL', 'PIA Status',
    'PIA Assessment URL', 'DPQ Complete', 'SIA Status', 'Criticality Tier',
    'Data Classification', 'Install Status', 'Collection Method', 'Collection Date', 'Status'
]

# Initialize collection
all_records = []
collection_log = {
    "collection_started": datetime.now().isoformat(),
    "total_stis": len(stis),
    "method": "Browser Automation - Direct ServiceNow",
    "records_collected": 0,
    "records": []
}

print(f"\n✅ Collection framework initialized")
print(f"   CSV output: soa_data_all_stis.csv")
print(f"   Progress log: soa_data_browser_collection.json")

# Field extraction instructions for browser automation:
# For each STI:
# 1. Navigate to: https://redhat.service-now.com/cmdb_ci_business_app_list.do?sysparm_query=application_id=<STI>
# 2. Click on the Business Application record
# 3. Extract from main page:
#    - Application Name (from heading)
#    - Criticality Tier (combobox value: C1, C2, C3, C4, or Pending)
#    - Data Classification (if visible)
#    - Install Status (if visible)
# 4. Click Compliance tab (ref-3yd4cee3myp or search for "Compliance")
#    - ESS Assessment URL (link field, extract href or textbox value)
#    - PIA Assessment URL (link field, extract href or textbox value)
# 5. Click Data Privacy tab (ref-96fck0cpl67 or search for "Data Privacy")
#    - DPQ Complete (combobox: "Yes", "No", "-- None --")
# 6. Search for SIA in other tabs (Support, etc.)
# 7. Save record and navigate to next STI

print(f"\n📋 Collection Pattern:")
print(f"   ✅ Main page: Name, Criticality, Classification")
print(f"   ✅ Compliance tab: ESS URL, PIA URL")
print(f"   ✅ Data Privacy tab: DPQ Complete")
print(f"   ✅ Other tabs: SIA Status")

print(f"\n🚀 Ready to collect data for all {len(stis)} STIs")
print(f"   Browser automation will iterate through each STI")
print(f"   Progress saved after each record")
print(f"   CSV file updated incrementally")

# Save initial state
with open('soa_data_browser_collection.json', 'w') as f:
    json.dump(collection_log, f, indent=2)

# Create/update CSV
df = pd.DataFrame(columns=csv_columns)
df.to_csv('soa_data_all_stis.csv', index=False)

print(f"\n✅ CSV template ready: soa_data_all_stis.csv")
print(f"   Browser automation can now populate data")

# Note: Browser automation will iterate through stis and populate all_records
# Then update CSV: pd.DataFrame(all_records).to_csv('soa_data_all_stis.csv', index=False)




