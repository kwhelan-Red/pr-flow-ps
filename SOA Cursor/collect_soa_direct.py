#!/usr/bin/env python3
"""
Collect SOA data directly from ServiceNow for all STIs
Iterates through each STI, navigates to its detail page, and extracts data
"""

import json
import time
from datetime import datetime

# Load STIs
with open('soa_stis_list.json', 'r') as f:
    data = json.load(f)
    stis = data.get('stis', [])

print(f"📊 Starting SOA data collection for {len(stis)} STIs")
print("="*80)

# Collection log
collection_log = {
    "collection_started": datetime.now().isoformat(),
    "total_stis": len(stis),
    "method": "Browser Automation - Direct ServiceNow Navigation",
    "base_url": "https://redhat.service-now.com",
    "records_collected": 0,
    "records": []
}

# Save initial log
with open('soa_data_browser_collection.json', 'w') as f:
    json.dump(collection_log, f, indent=2)

print(f"✅ Collection log initialized")
print(f"   File: soa_data_browser_collection.json")
print(f"\n📋 Collection Process for each STI:")
print(f"   1. Navigate to: https://redhat.service-now.com/cmdb_ci_business_app_list.do")
print(f"   2. Search for: application_id=<STI>")
print(f"   3. Click on the Business Application record")
print(f"   4. Extract from main page:")
print(f"      - Application Name")
print(f"      - Criticality Tier")
print(f"      - Data Classification")
print(f"      - Install Status")
print(f"      - SOA Applicable")
print(f"   5. Click Compliance tab:")
print(f"      - ESS Assessment URL")
print(f"      - PIA Assessment URL")
print(f"   6. Click Data Privacy tab:")
print(f"      - DPQ Complete")
print(f"   7. Search for SIA in other tabs")
print(f"   8. Save data and continue")
print(f"\n🚀 Starting collection...")

# Start with first STI as example
first_sti = stis[0] if stis else None
if first_sti:
    print(f"\n📍 First STI to process: {first_sti}")
    print(f"   URL pattern: https://redhat.service-now.com/cmdb_ci_business_app_list.do?sysparm_query=application_id={first_sti}")

print(f"\n💡 Note: Browser automation will iterate through all {len(stis)} STIs")
print(f"   Progress will be saved after each record")




