#!/usr/bin/env python3
"""
Comprehensive SOA Data Collection from ServiceNow
Supports multiple collection methods: Export processing, Browser automation, API
"""

import pandas as pd
import json
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import os

def load_stis(stis_file: str = "soa_stis_list.json") -> List[str]:
    """Load STI list from JSON file"""
    try:
        with open(stis_file, 'r') as f:
            data = json.load(f)
            return data.get('stis', [])
    except FileNotFoundError:
        print(f"❌ Error: {stis_file} not found")
        print("   Run collect_soa_data.py first to collect STI list")
        sys.exit(1)

def process_servicenow_export(csv_file: str, stis: List[str], output_file: str):
    """
    Process ServiceNow CSV export to extract SOA data for all STIs
    
    This is the RECOMMENDED method - fastest and most reliable
    """
    print(f"📊 Processing ServiceNow export: {csv_file}")
    
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return None
    
    print(f"✅ Loaded {len(df)} records from export\n")
    print(f"Columns: {list(df.columns)[:20]}...")  # Show first 20 columns
    
    # Identify key columns - more comprehensive matching
    app_id_col = None
    name_col = None
    soa_cols = []
    ess_cols = []
    pia_cols = []
    sia_cols = []
    criticality_col = None
    classification_col = None
    install_status_col = None
    
    for col in df.columns:
        col_lower = str(col).lower().strip()
        
        # Application ID / CMDB ID
        if app_id_col is None:
            if 'application id' in col_lower or 'app id' == col_lower:
                app_id_col = col
            elif 'cmdb' in col_lower and 'id' in col_lower:
                app_id_col = col
            elif col_lower == 'id' and 'application' in ' '.join(df.columns).lower():
                app_id_col = col
        
        # Application Name
        if name_col is None:
            if 'application name' in col_lower or 'app name' == col_lower:
                name_col = col
            elif 'name' == col_lower and 'application' in ' '.join(df.columns).lower():
                name_col = col
        
        # SOA columns
        if 'soa' in col_lower:
            soa_cols.append(col)
        
        # ESS columns
        if 'ess' in col_lower or 'enterprise security' in col_lower:
            ess_cols.append(col)
        if 'security (ess) assessment' in col_lower or 'ess assessment url' in col_lower:
            ess_cols.append(col)
        
        # PIA columns
        if 'pia' in col_lower or 'privacy impact' in col_lower:
            pia_cols.append(col)
        if 'privacy (pia) assessment' in col_lower or 'pia assessment url' in col_lower:
            pia_cols.append(col)
        if 'dpq complete' in col_lower or 'dpq' in col_lower:
            pia_cols.append(col)
        
        # SIA columns
        if 'sia' in col_lower or 'service impact' in col_lower:
            sia_cols.append(col)
        
        # Criticality
        if criticality_col is None:
            if 'criticality' in col_lower or 'tier' in col_lower:
                criticality_col = col
        
        # Data Classification
        if classification_col is None:
            if 'data classification' in col_lower or 'classification' == col_lower:
                classification_col = col
        
        # Install Status
        if install_status_col is None:
            if 'install status' in col_lower or 'status' == col_lower:
                install_status_col = col
    
    print(f"\nIdentified columns:")
    print(f"  Application ID: {app_id_col}")
    print(f"  Name: {name_col}")
    print(f"  SOA columns: {soa_cols}")
    print(f"  ESS columns: {ess_cols}")
    print(f"  PIA columns: {pia_cols}")
    print(f"  SIA columns: {sia_cols}")
    print(f"  Criticality: {criticality_col}")
    print(f"  Data Classification: {classification_col}")
    print(f"  Install Status: {install_status_col}\n")
    
    # Show sample of available columns if key ones not found
    if not app_id_col:
        print("⚠️  WARNING: Could not find Application ID column")
        print("Available columns (first 30):")
        for i, col in enumerate(df.columns[:30], 1):
            print(f"  {i}. {col}")
        if len(df.columns) > 30:
            print(f"  ... and {len(df.columns) - 30} more columns")
        print()
    
    if not app_id_col:
        print("❌ Could not find Application ID column")
        print("Available columns:")
        for col in df.columns:
            print(f"  - {col}")
        return None
    
    # Extract data for each STI
    results = []
    stis_found = set()
    
    for sti in stis:
        # Search for STI in Application ID column
        matching_rows = df[df[app_id_col].astype(str).str.contains(sti, case=False, na=False)]
        
        if len(matching_rows) > 0:
            row = matching_rows.iloc[0]  # Take first match
            
            app_name = str(row.get(name_col, '')).strip() if name_col and pd.notna(row.get(name_col)) else ''
            
            # Extract SOA data - try multiple columns for each field
            def get_field_value(cols, default=''):
                """Get value from first available column"""
                for col in cols:
                    if col and pd.notna(row.get(col)):
                        val = str(row.get(col)).strip()
                        if val and val.lower() not in ['nan', 'none', '']:
                            return val
                return default
            
            def get_field_value_by_pattern(pattern, default=''):
                """Search all columns for pattern"""
                for col in df.columns:
                    if pattern in str(col).lower():
                        val = row.get(col, '')
                        if pd.notna(val):
                            val_str = str(val).strip()
                            if val_str and val_str.lower() not in ['nan', 'none', '']:
                                return val_str
                return default
            
            # Extract ESS URL
            ess_url = get_field_value_by_pattern('ess assessment url', '')
            if not ess_url:
                ess_url = get_field_value_by_pattern('security (ess)', '')
            
            # Extract PIA URL
            pia_url = get_field_value_by_pattern('pia assessment url', '')
            if not pia_url:
                pia_url = get_field_value_by_pattern('privacy (pia)', '')
            
            # Extract DPQ Complete
            dpq_complete = get_field_value_by_pattern('dpq complete', '')
            
            # Extract SOA Status
            soa_status = get_field_value_by_pattern('soa status', '')
            
            soa_data = {
                "STI": sti,
                "CMDB ID": str(row.get(app_id_col, sti)).strip() if app_id_col else sti,
                "Application Name": app_name if app_name else get_field_value_by_pattern('name', ''),
                "SOA Applicable": get_field_value(soa_cols, ''),
                "SOA Status": soa_status,
                "ESS Self-Assessment Status": get_field_value(ess_cols, ''),
                "ESS Assessment URL": ess_url,
                "PIA Status": get_field_value(pia_cols, ''),
                "PIA Assessment URL": pia_url,
                "DPQ Complete": dpq_complete,
                "SIA Status": get_field_value(sia_cols, ''),
                "Criticality Tier": str(row.get(criticality_col, '')).strip() if criticality_col and pd.notna(row.get(criticality_col)) else '',
                "Data Classification": str(row.get(classification_col, '')).strip() if classification_col and pd.notna(row.get(classification_col)) else '',
                "Install Status": str(row.get(install_status_col, '')).strip() if install_status_col and pd.notna(row.get(install_status_col)) else '',
                "Collection Method": "ServiceNow Export",
                "Collection Date": datetime.now().isoformat(),
                "Status": "Found"
            }
            
            # Additional field extraction - check all columns for any relevant data
            for col in df.columns:
                col_lower = str(col).lower()
                val = row.get(col, '')
                if pd.notna(val):
                    val_str = str(val).strip()
                    if val_str and val_str.lower() not in ['nan', 'none', '']:
                        # Fill in any empty fields
                        if not soa_data["Criticality Tier"] and ('criticality' in col_lower or 'tier' in col_lower):
                            soa_data["Criticality Tier"] = val_str
                        if not soa_data["Data Classification"] and ('classification' in col_lower):
                            soa_data["Data Classification"] = val_str
                        if not soa_data["Install Status"] and ('install status' in col_lower or ('status' in col_lower and 'install' in col_lower)):
                            soa_data["Install Status"] = val_str
                        if not soa_data["SOA Status"] and 'soa' in col_lower and 'status' in col_lower:
                            soa_data["SOA Status"] = val_str
            
            results.append(soa_data)
            stis_found.add(sti)
        else:
            # STI not found in export
            results.append({
                "STI": sti,
                "CMDB ID": sti,
                "Application Name": "",
                "Status": "Not Found in Export",
                "Collection Method": "ServiceNow Export",
                "Collection Date": datetime.now().isoformat()
            })
    
    print(f"✅ Found data for {len(stis_found)}/{len(stis)} STIs in export")
    
    # Save results
    output_data = {
        "collection_started": datetime.now().isoformat(),
        "collection_method": "ServiceNow CSV Export",
        "source_file": csv_file,
        "total_stis": len(stis),
        "stis_found": len(stis_found),
        "stis_not_found": len(stis) - len(stis_found),
        "records": results
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    # Create DataFrame
    df_results = pd.DataFrame(results)
    
    # Create CSV file
    csv_file = output_file.replace('.json', '.csv')
    df_results.to_csv(csv_file, index=False)
    print(f"✅ CSV file created: {csv_file}")
    
    # Also create Excel file
    excel_file = output_file.replace('.json', '.xlsx')
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df_results.to_excel(writer, sheet_name='SOA Data', index=False)
        
        # Create summary sheet
        summary_data = []
        for sti in stis:
            sti_records = [r for r in results if r.get('STI') == sti]
            if sti_records:
                record = sti_records[0]
                summary_data.append({
                    "STI": sti,
                    "Found": "Yes" if record.get('Status') == 'Found' else "No",
                    "Application Name": record.get('Application Name', ''),
                    "SOA Applicable": record.get('SOA Applicable', ''),
                    "ESS Status": record.get('ESS Self-Assessment Status', ''),
                    "PIA Status": record.get('PIA Status', ''),
                    "SIA Status": record.get('SIA Status', '')
                })
            else:
                summary_data.append({
                    "STI": sti,
                    "Found": "No",
                    "Application Name": "",
                    "SOA Applicable": "",
                    "ESS Status": "",
                    "PIA Status": "",
                    "SIA Status": ""
                })
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='STI Summary', index=False)
        
        # Also create CSV for summary
        summary_csv = output_file.replace('.json', '_summary.csv')
        df_summary.to_csv(summary_csv, index=False)
        print(f"✅ Summary CSV created: {summary_csv}")
    
    print(f"\n✅ Results saved:")
    print(f"   JSON: {output_file}")
    print(f"   CSV: {csv_file}")
    print(f"   Summary CSV: {summary_csv}")
    print(f"   Excel: {excel_file}")
    
    return output_data

def main():
    parser = argparse.ArgumentParser(description="Collect SOA data from ServiceNow for all STIs")
    parser.add_argument("--method", choices=['export', 'browser', 'api'], default='export',
                       help="Collection method (default: export)")
    parser.add_argument("--export-file", help="ServiceNow CSV export file (for export method)")
    parser.add_argument("--stis-file", default="soa_stis_list.json", help="STI list JSON file")
    parser.add_argument("--output", default="soa_data_all_stis.json", help="Output file")
    args = parser.parse_args()
    
    print("="*80)
    print("SOA DATA COLLECTION FROM SERVICENOW")
    print("="*80)
    print()
    
    # Load STIs
    stis = load_stis(args.stis_file)
    print(f"📋 Loaded {len(stis)} STIs from {args.stis_file}\n")
    
    if args.method == 'export':
        if not args.export_file:
            print("❌ Error: --export-file required for export method")
            print("\n📝 Instructions:")
            print("1. Go to ServiceNow Business Applications list")
            print("2. Filter: SOA Applicable = true")
            print("3. Click 'Actions on selected rows...' → Export")
            print("4. Export to CSV (all fields)")
            print("5. Run: python3 get_soa_data.py --method export --export-file /path/to/export.csv")
            sys.exit(1)
        
        if not os.path.exists(args.export_file):
            print(f"❌ Error: Export file not found: {args.export_file}")
            sys.exit(1)
        
        process_servicenow_export(args.export_file, stis, args.output)
    
    elif args.method == 'browser':
        print("🌐 Browser automation method")
        print("⚠️  This requires SSO authentication and may be slow")
        print("💡 Recommendation: Use export method instead")
        # Browser automation would go here
    
    elif args.method == 'api':
        print("🔌 API method")
        print("⚠️  Requires ServiceNow API credentials")
        print("💡 Recommendation: Use export method instead")
        # API calls would go here

if __name__ == "__main__":
    main()

