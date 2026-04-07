#!/usr/bin/env python3
"""
Collect ESS, PIA, SIA status from ServiceNow Business Applications
This script will be used to systematically collect data from all 283 records
"""

import json
from datetime import datetime

# Collection data structure
collection_data = {
    "started": datetime.now().isoformat(),
    "total_records": 283,
    "method": "Browser automation - Compliance and Data Privacy tabs",
    "field_mapping": {
        "ESS": "Compliance tab - Security (ESS) assessment URL",
        "PIA": "Compliance tab - Privacy (PIA) assessment URL + Data Privacy tab - DPQ Complete",
        "SIA": "To be determined"
    },
    "records": []
}

def add_record(cmdb_id, app_name, ess_url, ess_status, pia_url, pia_status, sia_status, record_num):
    """Add a collected record"""
    collection_data["records"].append({
        "Record Number": record_num,
        "CMDB ID": cmdb_id,
        "Application Name": app_name,
        "ESS Assessment URL": ess_url,
        "ESS Status": ess_status,
        "PIA Assessment URL": pia_url,
        "PIA Status": pia_status,
        "SIA Status": sia_status,
        "Collected At": datetime.now().isoformat()
    })
    save_progress()

def save_progress():
    """Save collection progress"""
    with open('ess_pia_sia_collection_log.json', 'w') as f:
        json.dump(collection_data, f, indent=2)
    print(f"✅ Progress saved: {len(collection_data['records'])}/{collection_data['total_records']} records")

def determine_status_from_url(url_field):
    """Determine status based on URL field presence"""
    if not url_field or url_field.strip() == "" or url_field == "N/A":
        return "Not Started"
    elif "http" in str(url_field).lower():
        return "In Progress"  # URL present suggests assessment exists
    else:
        return "Unknown"

if __name__ == "__main__":
    print("="*80)
    print("ESS, PIA, SIA STATUS COLLECTION")
    print("="*80)
    print()
    print("Collection method:")
    print("  1. Navigate to Business Application detail page")
    print("  2. Click Compliance tab")
    print("  3. Extract ESS assessment URL")
    print("  4. Extract PIA assessment URL")
    print("  5. Click Data Privacy tab")
    print("  6. Extract DPQ Complete status")
    print("  7. Determine status from URL presence")
    print("  8. Navigate to next record")
    print()
    print(f"Total records to collect: {collection_data['total_records']}")
    print(f"Records collected: {len(collection_data['records'])}")
    print()
    print("Progress saved to: ess_pia_sia_collection_log.json")




