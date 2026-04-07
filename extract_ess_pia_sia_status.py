#!/usr/bin/env python3
"""
Extract ESS, PIA, SIA status for each CMDB ID from ServiceNow export
Processes exported data to show assessment status for all 283 SOA-applicable applications
"""

import pandas as pd
import sys
import argparse
import re

def find_status_columns(df):
    """Find columns related to ESS, PIA, SIA status"""
    
    # Common column name patterns
    ess_patterns = [
        r'ess.*status',
        r'enterprise.*security.*status',
        r'ess.*assessment',
        r'ess.*self.*assessment',
        r'ess.*complete',
        r'u_ess'
    ]
    
    pia_patterns = [
        r'pia.*status',
        r'privacy.*impact.*status',
        r'pia.*assessment',
        r'pia.*complete',
        r'u_pia'
    ]
    
    sia_patterns = [
        r'sia.*status',
        r'service.*impact.*status',
        r'sia.*assessment',
        r'sia.*complete',
        r'u_sia'
    ]
    
    ess_cols = []
    pia_cols = []
    sia_cols = []
    
    for col in df.columns:
        col_lower = col.lower()
        
        for pattern in ess_patterns:
            if re.search(pattern, col_lower):
                ess_cols.append(col)
                break
        
        for pattern in pia_patterns:
            if re.search(pattern, col_lower):
                pia_cols.append(col)
                break
        
        for pattern in sia_patterns:
            if re.search(pattern, col_lower):
                sia_cols.append(col)
                break
    
    return ess_cols, pia_cols, sia_cols

def process_servicenow_export(csv_file, output_file):
    """Process ServiceNow export to extract ESS, PIA, SIA status"""
    
    print(f"Reading ServiceNow export: {csv_file}")
    try:
        # Try different encodings
        try:
            df = pd.read_csv(csv_file, encoding='utf-8')
        except:
            df = pd.read_csv(csv_file, encoding='latin-1')
    except FileNotFoundError:
        print(f"❌ Error: File not found: {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)
    
    print(f"✅ Loaded {len(df)} records\n")
    
    # Show available columns
    print("Available columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i:2d}. {col}")
    print()
    
    # Find Application ID column
    app_id_col = None
    app_id_patterns = [
        r'application.*id',
        r'cmdb.*id',
        r'app.*id',
        r'^id$'
    ]
    
    for col in df.columns:
        col_lower = col.lower()
        for pattern in app_id_patterns:
            if re.search(pattern, col_lower):
                app_id_col = col
                break
        if app_id_col:
            break
    
    if not app_id_col:
        print("❌ Could not find Application ID column")
        print("Please specify with --id-column")
        sys.exit(1)
    
    print(f"✅ Using '{app_id_col}' for Application IDs\n")
    
    # Find ESS, PIA, SIA columns
    ess_cols, pia_cols, sia_cols = find_status_columns(df)
    
    print(f"Found status columns:")
    print(f"  ESS: {ess_cols if ess_cols else 'NOT FOUND'}")
    print(f"  PIA: {pia_cols if pia_cols else 'NOT FOUND'}")
    print(f"  SIA: {sia_cols if sia_cols else 'NOT FOUND'}")
    print()
    
    # If columns not found, show all columns and ask user
    if not ess_cols and not pia_cols and not sia_cols:
        print("⚠️  Could not auto-detect ESS, PIA, SIA columns")
        print("Please check the column names above and specify manually:")
        print("  --ess-column 'Column Name'")
        print("  --pia-column 'Column Name'")
        print("  --sia-column 'Column Name'")
        return
    
    # Get name column
    name_col = None
    for col in df.columns:
        if col.lower() in ['name', 'application name', 'app name']:
            name_col = col
            break
    
    # Process each record
    output_data = []
    for idx, row in df.iterrows():
        app_id = str(row[app_id_col]).strip() if pd.notna(row[app_id_col]) else ''
        app_name = str(row[name_col]).strip() if name_col and pd.notna(row.get(name_col)) else ''
        
        if not app_id or app_id == 'nan':
            continue
        
        # Get ESS status
        ess_status = 'Not Found'
        if ess_cols:
            for col in ess_cols:
                val = row.get(col, '')
                if pd.notna(val) and str(val).strip() and str(val).strip().lower() != 'nan':
                    ess_status = str(val).strip()
                    break
        
        # Get PIA status
        pia_status = 'Not Found'
        if pia_cols:
            for col in pia_cols:
                val = row.get(col, '')
                if pd.notna(val) and str(val).strip() and str(val).strip().lower() != 'nan':
                    pia_status = str(val).strip()
                    break
        
        # Get SIA status
        sia_status = 'Not Found'
        if sia_cols:
            for col in sia_cols:
                val = row.get(col, '')
                if pd.notna(val) and str(val).strip() and str(val).strip().lower() != 'nan':
                    sia_status = str(val).strip()
                    break
        
        output_data.append({
            'CMDB ID': app_id,
            'Application Name': app_name,
            'ESS Self-Assessment Status': ess_status,
            'PIA Status': pia_status,
            'SIA Status': sia_status
        })
    
    # Create DataFrame
    df_output = pd.DataFrame(output_data)
    df_output = df_output.sort_values('CMDB ID')
    
    # Calculate summary statistics
    total = len(df_output)
    ess_complete = len(df_output[df_output['ESS Self-Assessment Status'].str.contains('Complete|Yes|Pass|Approved', case=False, na=False)])
    ess_in_progress = len(df_output[df_output['ESS Self-Assessment Status'].str.contains('Progress|Pending|In Progress', case=False, na=False)])
    ess_not_found = len(df_output[df_output['ESS Self-Assessment Status'] == 'Not Found'])
    
    pia_complete = len(df_output[df_output['PIA Status'].str.contains('Complete|Yes|Pass|Approved', case=False, na=False)])
    pia_not_found = len(df_output[df_output['PIA Status'] == 'Not Found'])
    
    sia_complete = len(df_output[df_output['SIA Status'].str.contains('Complete|Yes|Pass|Approved', case=False, na=False)])
    sia_not_found = len(df_output[df_output['SIA Status'] == 'Not Found'])
    
    # Save to Excel
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Main data sheet
        df_output.to_excel(writer, sheet_name='ESS_PIA_SIA_Status', index=False)
        
        # Summary sheet
        summary_data = [
            {'Metric': 'Total CMDB IDs', 'Count': total},
            {'Metric': 'ESS - Complete', 'Count': ess_complete, 'Percentage': f'{(ess_complete/total*100):.1f}%'},
            {'Metric': 'ESS - In Progress', 'Count': ess_in_progress, 'Percentage': f'{(ess_in_progress/total*100):.1f}%'},
            {'Metric': 'ESS - Not Found', 'Count': ess_not_found, 'Percentage': f'{(ess_not_found/total*100):.1f}%'},
            {'Metric': 'PIA - Complete', 'Count': pia_complete, 'Percentage': f'{(pia_complete/total*100):.1f}%'},
            {'Metric': 'PIA - Not Found', 'Count': pia_not_found, 'Percentage': f'{(pia_not_found/total*100):.1f}%'},
            {'Metric': 'SIA - Complete', 'Count': sia_complete, 'Percentage': f'{(sia_complete/total*100):.1f}%'},
            {'Metric': 'SIA - Not Found', 'Count': sia_not_found, 'Percentage': f'{(sia_not_found/total*100):.1f}%'},
        ]
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False)
        
        # Adjust column widths
        worksheet = writer.sheets['ESS_PIA_SIA_Status']
        worksheet.column_dimensions['A'].width = 15  # CMDB ID
        worksheet.column_dimensions['B'].width = 40  # Application Name
        worksheet.column_dimensions['C'].width = 30  # ESS Status
        worksheet.column_dimensions['D'].width = 20  # PIA Status
        worksheet.column_dimensions['E'].width = 20  # SIA Status
        
        worksheet_summary = writer.sheets['Summary']
        worksheet_summary.column_dimensions['A'].width = 25
        worksheet_summary.column_dimensions['B'].width = 15
        worksheet_summary.column_dimensions['C'].width = 15
    
    print(f"\n✅ Excel file created: {output_file}")
    print(f"   Total CMDB IDs processed: {len(output_data)}")
    print(f"\n📊 Summary:")
    print(f"   ESS Complete: {ess_complete} ({(ess_complete/total*100):.1f}%)")
    print(f"   ESS In Progress: {ess_in_progress} ({(ess_in_progress/total*100):.1f}%)")
    print(f"   PIA Complete: {pia_complete} ({(pia_complete/total*100):.1f}%)")
    print(f"   SIA Complete: {sia_complete} ({(sia_complete/total*100):.1f}%)")
    print(f"\nFirst 10 records:")
    print(df_output.head(10).to_string(index=False))

def main():
    parser = argparse.ArgumentParser(description="Extract ESS, PIA, SIA status from ServiceNow export")
    parser.add_argument("csv_file", help="Path to ServiceNow CSV export file")
    parser.add_argument("--output", default="CMDB_ESS_PIA_SIA_Status.xlsx", help="Output Excel file name")
    parser.add_argument("--id-column", help="Name of the Application ID column (auto-detected if not specified)")
    parser.add_argument("--ess-column", help="Name of the ESS status column (auto-detected if not specified)")
    parser.add_argument("--pia-column", help="Name of the PIA status column (auto-detected if not specified)")
    parser.add_argument("--sia-column", help="Name of the SIA status column (auto-detected if not specified)")
    args = parser.parse_args()
    
    print("="*80)
    print("EXTRACT ESS, PIA, SIA STATUS FOR CMDB IDs")
    print("="*80)
    print()
    
    process_servicenow_export(args.csv_file, args.output)

if __name__ == "__main__":
    main()
