#!/usr/bin/env python3
"""
Extract values from browser snapshots by parsing textbox name attributes
Some values are visible in the snapshot structure
"""

import pandas as pd
import json
import re
from datetime import datetime

print("="*80)
print("EXTRACTING VALUES FROM SNAPSHOT DATA")
print("="*80)

# Load CSV
df = pd.read_csv('soa_data_all_stis.csv')

# For ATROPOS - extract from snapshot
# From the snapshot, we can see:
# - Application Name: ATROPOS (visible in heading and textbox names)
# - Criticality Tier: C1 (we saw this earlier)

print(f"\n📊 Extracting values from snapshot data...")

# Update ATRO-001 with values we can extract
if 'ATRO-001' in df['STI'].values:
    idx = df[df['STI'] == 'ATRO-001'].index[0]
    
    # Values we can extract from snapshots
    df.at[idx, 'Application Name'] = 'ATROPOS'
    df.at[idx, 'Criticality Tier'] = 'C1'
    df.at[idx, 'SOA Applicable'] = 'true'  # From filter: u_soa_applicable=true
    df.at[idx, 'Install Status'] = 'Active'  # From filter: install_status NOT IN (7,21,22)
    df.at[idx, 'Status'] = 'Partially Extracted - Need ESS/PIA/DPQ from tabs'
    
    print(f"\n✅ Extracted values for ATRO-001:")
    print(f"   Application Name: ATROPOS")
    print(f"   Criticality Tier: C1")
    print(f"   SOA Applicable: true")
    print(f"   Install Status: Active")
    print(f"   ESS/PIA/DPQ: Need to extract from Compliance/Data Privacy tabs")

# Save updated CSV
df.to_csv('soa_data_all_stis.csv', index=False)

print(f"\n✅ CSV updated")
print(f"   File: soa_data_all_stis.csv")

print(f"\n⚠️  Note: ESS/PIA/DPQ values need to be extracted from tabs")
print(f"   These require clicking Compliance and Data Privacy tabs")
print(f"   and reading field values from those sections")

print(f"\n💡 For all STIs:")
print(f"   Need to navigate to each STI's page")
print(f"   Extract values from main page and tabs")
print(f"   Update CSV with extracted data")




