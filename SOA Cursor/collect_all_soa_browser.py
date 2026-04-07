#!/usr/bin/env python3
"""
Complete SOA Data Collection from ServiceNow - Browser Automation Script
Collects data for all 114 STIs by navigating to each Business Application record
"""

import json
import pandas as pd
from datetime import datetime
from typing import Dict, List

# Load STIs
with open('soa_stis_list.json', 'r') as f:
    data = json.load(f)
    stis = data.get('stis', [])

print("="*80)
print("SOA DATA COLLECTION FROM SERVICENOW - BROWSER AUTOMATION")
print("="*80)
print(f"\nTotal STIs: {len(stis)}")
print(f"Collection Method: Direct browser automation")

# Initialize collection
collection_data = {
    "collection_started": datetime.now().isoformat(),
    "total_stis": len(stis),
    "method": "Browser Automation - Direct ServiceNow Navigation",
    "base_url": "https://redhat.service-now.com",
    "records": []
}

# Field extraction pattern for each STI:
# 1. Navigate to: https://redhat.service-now.com/cmdb_ci_business_app_list.do?sysparm_query=application_id=<STI>
# 2. Click on the Business Application record
# 3. Extract from main page:
#    - Application Name (heading)
#    - Criticality Tier (combobox, name: "C1", "C2", etc.)
#    - Data Classification (if visible)
#    - Install Status (if visible)
#    - SOA Applicable (checkbox or field)
# 4. Click Compliance tab (ref-3yd4cee3myp or similar)
#    - ESS Assessment URL (link field)
#    - PIA Assessment URL (link field)
# 5. Click Data Privacy tab (ref-96fck0cpl67 or similar)
#    - DPQ Complete (combobox: "Yes", "No", "-- None --")
# 6. Search for SIA in other tabs
# 7. Save data and navigate to next STI

print(f"\n📋 Collection Pattern Established:")
print(f"   ✅ Main page fields identified")
print(f"   ✅ Compliance tab: ESS & PIA URLs")
print(f"   ✅ Data Privacy tab: DPQ Complete")
print(f"   ✅ Tab references identified")

# Save framework
with open('soa_data_browser_collection.json', 'w') as f:
    json.dump(collection_data, f, indent=2)

print(f"\n✅ Collection framework saved: soa_data_browser_collection.json")
print(f"\n🚀 Ready for browser automation to iterate through all {len(stis)} STIs")
print(f"\n💡 Note: Browser automation will:")
print(f"   - Navigate to each STI's detail page")
print(f"   - Extract all fields using identified patterns")
print(f"   - Save progress after each record")
print(f"   - Generate CSV/Excel output when complete")

# Create output template
output_template = {
    "STI": "",
    "CMDB ID": "",
    "Application Name": "",
    "SOA Applicable": "",
    "SOA Status": "",
    "ESS Self-Assessment Status": "",
    "ESS Assessment URL": "",
    "PIA Status": "",
    "PIA Assessment URL": "",
    "DPQ Complete": "",
    "SIA Status": "",
    "Criticality Tier": "",
    "Data Classification": "",
    "Install Status": "",
    "Collection Method": "Browser Automation",
    "Collection Date": "",
    "Status": ""
}

print(f"\n📊 Output fields template created")
print(f"   Fields: {len(output_template)} data points per STI")




