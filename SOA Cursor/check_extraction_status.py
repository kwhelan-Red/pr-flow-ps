#!/usr/bin/env python3
"""
Check extraction status and progress
"""

import pandas as pd
import json
import sys

def check_status():
    """Check extraction status"""
    try:
        df = pd.read_csv('soa_data_all_stis.csv')
    except FileNotFoundError:
        print("❌ Error: soa_data_all_stis.csv not found")
        return
    
    total = len(df)
    extracted = len(df[df['Status'].str.contains('Extracted', na=False)])
    pending = total - extracted
    
    print("="*80)
    print("EXTRACTION STATUS")
    print("="*80)
    print(f"\n📊 Overall Status:")
    print(f"   Total STIs: {total}")
    print(f"   Extracted: {extracted} ({extracted/total*100:.1f}%)")
    print(f"   Pending: {pending} ({pending/total*100:.1f}%)")
    
    # Check field completion
    fields_to_check = [
        'Application Name',
        'Criticality Tier',
        'ESS Assessment URL',
        'PIA Assessment URL',
        'DPQ Complete'
    ]
    
    print(f"\n📋 Field Completion:")
    for field in fields_to_check:
        if field in df.columns:
            filled = len(df[df[field].notna() & (df[field] != 'empty value') & (df[field] != '')])
            print(f"   {field}: {filled}/{total} ({filled/total*100:.1f}%)")
    
    # Show pending STIs
    if pending > 0:
        pending_stis = df[~df['Status'].str.contains('Extracted', na=False)]['STI'].tolist()
        print(f"\n⏳ Pending STIs (first 10):")
        for sti in pending_stis[:10]:
            print(f"   - {sti}")
        if len(pending_stis) > 10:
            print(f"   ... and {len(pending_stis) - 10} more")

if __name__ == "__main__":
    check_status()




