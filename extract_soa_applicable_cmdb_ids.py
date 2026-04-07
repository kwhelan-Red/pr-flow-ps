#!/usr/bin/env python3
"""
Extract CMDB IDs that need SOA assessments from ServiceNow export
Processes a CSV export from the ServiceNow Business Applications list
"""

import pandas as pd
import sys
import argparse

def extract_cmdb_ids_from_servicenow_export(csv_file, output_file):
    """Extract CMDB IDs from ServiceNow CSV export"""
    
    print(f"Reading ServiceNow export: {csv_file}")
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)
    
    print(f"✅ Loaded {len(df)} records\n")
    
    # Identify the Application ID column (could be named differently)
    app_id_columns = [col for col in df.columns if 'application' in col.lower() and 'id' in col.lower()]
    app_id_columns.extend([col for col in df.columns if 'cmdb' in col.lower() and 'id' in col.lower()])
    app_id_columns.extend([col for col in df.columns if col.lower() in ['application id', 'app id', 'cmdb id', 'id']])
    
    if not app_id_columns:
        print("Available columns:")
        for col in df.columns:
            print(f"  - {col}")
        print("\n❌ Could not find Application ID column")
        print("Please specify the column name with --id-column")
        sys.exit(1)
    
    app_id_col = app_id_columns[0]
    print(f"Using column: '{app_id_col}' for Application IDs\n")
    
    # Extract CMDB IDs
    cmdb_ids = df[app_id_col].dropna().unique()
    cmdb_ids = sorted([str(id).strip() for id in cmdb_ids if str(id).strip()])
    
    # Also get application names if available
    name_columns = [col for col in df.columns if 'name' in col.lower()]
    name_col = name_columns[0] if name_columns else None
    
    # Create output data
    output_data = []
    for idx, row in df.iterrows():
        app_id = str(row[app_id_col]).strip() if pd.notna(row[app_id_col]) else ''
        app_name = str(row[name_col]).strip() if name_col and pd.notna(row.get(name_col)) else ''
        
        if app_id:
            output_data.append({
                'CMDB ID': app_id,
                'Application Name': app_name,
                'Row Number': idx + 1
            })
    
    # Create DataFrame and sort
    df_output = pd.DataFrame(output_data)
    df_output = df_output.sort_values('CMDB ID')
    
    # Save to Excel
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # All CMDB IDs
        df_output.to_excel(writer, sheet_name='All CMDB IDs', index=False)
        
        # Summary
        summary_data = [{
            'Total CMDB IDs': len(cmdb_ids),
            'Unique CMDB IDs': len(set(cmdb_ids)),
            'Source File': csv_file
        }]
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        
        # Get worksheets to adjust column widths
        worksheet = writer.sheets['All CMDB IDs']
        worksheet.column_dimensions['A'].width = 15  # CMDB ID
        worksheet.column_dimensions['B'].width = 50  # Application Name
        worksheet.column_dimensions['C'].width = 12  # Row Number
    
    print(f"✅ Excel file created: {output_file}")
    print(f"   Total CMDB IDs: {len(cmdb_ids)}")
    print(f"   Unique CMDB IDs: {len(set(cmdb_ids))}")
    print(f"\nFirst 10 CMDB IDs:")
    for i, cmdb_id in enumerate(cmdb_ids[:10], 1):
        print(f"  {i:3d}. {cmdb_id}")
    if len(cmdb_ids) > 10:
        print(f"  ... and {len(cmdb_ids) - 10} more")

def main():
    parser = argparse.ArgumentParser(description="Extract CMDB IDs from ServiceNow export")
    parser.add_argument("csv_file", help="Path to ServiceNow CSV export file")
    parser.add_argument("--output", default="SOA_Applicable_CMDB_IDs.xlsx", help="Output Excel file name")
    parser.add_argument("--id-column", help="Name of the Application ID column (auto-detected if not specified)")
    args = parser.parse_args()
    
    print("="*80)
    print("EXTRACT CMDB IDs THAT NEED SOA ASSESSMENTS")
    print("="*80)
    print()
    
    extract_cmdb_ids_from_servicenow_export(args.csv_file, args.output)

if __name__ == "__main__":
    main()




