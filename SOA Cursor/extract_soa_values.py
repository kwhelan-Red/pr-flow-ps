#!/usr/bin/env python3
"""
Extract SOA data from ServiceNow page and populate CSV
Reads browser snapshots/logs to extract field values
"""

import pandas as pd
import json
import re
from datetime import datetime
from pathlib import Path

def extract_url_from_snapshot(snapshot_file, field_name):
    """Extract URL value from snapshot file"""
    try:
        with open(snapshot_file, 'r') as f:
            content = f.read()
            # Look for URL patterns near the field name
            pattern = rf'{re.escape(field_name)}.*?http[s]?://[^\s"<>]+'
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            if matches:
                # Extract URL from match
                url_match = re.search(r'http[s]?://[^\s"<>]+', matches[0])
                if url_match:
                    return url_match.group(0)
    except:
        pass
    return ''

def extract_field_value_from_snapshot(snapshot_file, field_label):
    """Extract field value from snapshot"""
    try:
        with open(snapshot_file, 'r') as f:
            content = f.read()
            # Look for field label followed by value
            # This is a simplified extraction - actual implementation would parse the snapshot structure
            pass
    except:
        pass
    return ''

# Get latest snapshot file
snapshot_dir = Path('/Users/kwhelan/.cursor/browser-logs')
snapshot_files = sorted(snapshot_dir.glob('snapshot-*.log'), key=lambda x: x.stat().st_mtime, reverse=True)
latest_snapshot = snapshot_files[0] if snapshot_files else None

print(f"📊 Extracting data from ServiceNow page")
print(f"   Latest snapshot: {latest_snapshot.name}")

# Extract ATROPOS data
atropos_data = {
    'STI': 'ATRO-001',
    'CMDB ID': 'ATRO-001',
    'Application Name': 'ATROPOS',
    'SOA Applicable': 'true',  # From filter: u_soa_applicable=true
    'SOA Status': '',
    'ESS Self-Assessment Status': '',
    'ESS Assessment URL': '',  # Need to extract from Compliance tab
    'PIA Status': '',
    'PIA Assessment URL': '',  # Need to extract from Compliance tab
    'DPQ Complete': '',  # Need to extract from Data Privacy tab
    'SIA Status': '',
    'Criticality Tier': 'C1',
    'Data Classification': '',
    'Install Status': 'Active',  # From filter: install_status NOT IN (7,21,22)
    'Collection Method': 'Browser Automation - Direct ServiceNow',
    'Collection Date': datetime.now().isoformat(),
    'Status': 'Data Extraction Needed'
}

print(f"\n⚠️  Note: Field values need to be extracted from browser page")
print(f"   Current snapshot shows field locations but not all values")
print(f"   Browser automation needs to read actual field values")

# Update CSV
df = pd.read_csv('soa_data_all_stis.csv')
# Update ATROPOS record
df.loc[df['STI'] == 'ATRO-001', 'Criticality Tier'] = 'C1'
df.loc[df['STI'] == 'ATRO-001', 'SOA Applicable'] = 'true'
df.loc[df['STI'] == 'ATRO-001', 'Install Status'] = 'Active'

df.to_csv('soa_data_all_stis.csv', index=False)

print(f"\n✅ Updated CSV with available data")
print(f"   Note: ESS/PIA URLs and DPQ Complete need browser automation")
print(f"   to read actual values from Compliance/Data Privacy tabs")




