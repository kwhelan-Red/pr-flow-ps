#!/usr/bin/env python3
"""
Collect all SOA data from ServiceNow for all STIs
Extracts SOA status, ESS, PIA, SIA, and related compliance information
"""

import pandas as pd
import sys
import argparse
import json
from datetime import datetime
from typing import Dict, List, Optional

def collect_all_stis():
    """Collect all STIs from various sources"""
    all_stis = set()
    sources = []
    
    # 1. From Secure Flow gaps Excel
    try:
        df_gaps = pd.read_excel('/Users/kwhelan/pr-flow-ps/Secure_Flow_SP_Gaps_Complete.xlsx', sheet_name='STI Summary')
        stis_from_gaps = set(df_gaps['STI'].dropna().unique())
        all_stis.update(stis_from_gaps)
        sources.append(('Secure Flow Gaps', len(stis_from_gaps)))
    except Exception as e:
        print(f'⚠️  Could not read Secure Flow gaps: {e}')
    
    # 2. From SOAR Excel files
    soar_files = [
        '/Users/kwhelan/pr-flow-ps/SOAR_STIs_and_CMDB_IDs.xlsx',
        '/Users/kwhelan/pr-flow-ps/SOAR_STIs_From_Open_Issues.xlsx'
    ]
    
    for file in soar_files:
        try:
            import os
            if os.path.exists(file):
                df_soar = pd.read_excel(file)
                if 'STI' in df_soar.columns:
                    stis_from_soar = set(df_soar['STI'].dropna().unique())
                    all_stis.update(stis_from_soar)
                    sources.append((os.path.basename(file), len(stis_from_soar)))
        except Exception as e:
            print(f'⚠️  Could not read {file}: {e}')
    
    return sorted(list(all_stis)), sources

def create_soa_data_template():
    """Create template for SOA data collection"""
    template = {
        "collection_started": datetime.now().isoformat(),
        "total_stis": 0,
        "collection_method": "ServiceNow Browser Automation",
        "data_fields": [
            "STI/CMDB ID",
            "Application Name",
            "SOA Status",
            "SOA Applicable",
            "ESS Self-Assessment Status",
            "ESS Assessment URL",
            "PIA Status",
            "PIA Assessment URL",
            "DPQ Complete",
            "SIA Status",
            "Criticality Tier",
            "Data Classification",
            "Install Status",
            "Last Updated"
        ],
        "records": []
    }
    return template

def main():
    parser = argparse.ArgumentParser(description="Collect all SOA data from ServiceNow for all STIs")
    parser.add_argument("--output", default="soa_data_collection.json", help="Output JSON file for collection log")
    parser.add_argument("--stis-file", help="Input file with STI list (optional, will collect from known sources)")
    args = parser.parse_args()
    
    print("="*80)
    print("SOA DATA COLLECTION FROM SERVICENOW")
    print("="*80)
    print()
    
    # Collect all STIs
    print("📋 Collecting STIs from various sources...")
    all_stis, sources = collect_all_stis()
    
    print(f"\n✅ Collected {len(all_stis)} unique STIs from:")
    for source_name, count in sources:
        print(f"   - {source_name}: {count} STIs")
    
    print(f"\n📊 Total unique STIs: {len(all_stis)}")
    print(f"   Sample: {all_stis[:10]}")
    
    # Create collection template
    collection_data = create_soa_data_template()
    collection_data["total_stis"] = len(all_stis)
    collection_data["stis"] = all_stis
    
    # Save collection template
    with open(args.output, 'w') as f:
        json.dump(collection_data, f, indent=2)
    
    print(f"\n✅ Collection template saved to: {args.output}")
    print(f"\n📝 Next steps:")
    print(f"   1. Navigate to ServiceNow Business Applications list")
    print(f"   2. Search for each STI/CMDB ID")
    print(f"   3. Extract SOA, ESS, PIA, SIA data")
    print(f"   4. Update {args.output} with collected data")
    print(f"\n💡 Tip: Use browser automation or ServiceNow API to automate collection")

if __name__ == "__main__":
    main()




