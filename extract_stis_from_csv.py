#!/usr/bin/env python3
"""
Extract ALL STIs and CMDB IDs from a Jira CSV export
Use this if you can export all SOAR issues (not just open ones) from Jira
"""

import pandas as pd
import re
import sys
import argparse

def extract_stis_from_csv(csv_file, output_file):
    """Extract all STIs from a Jira CSV export"""
    
    print(f"Reading CSV file: {csv_file}")
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)
    
    print(f"✅ Loaded {len(df)} issues from CSV\n")
    
    sti_pattern = r'\[([A-Z0-9]+-[0-9]+)\]'
    
    all_stis = set()
    sti_issue_map = {}
    excel_data = []
    
    print("Extracting STIs...")
    
    for idx, row in df.iterrows():
        summary = str(row.get('Summary', ''))
        key = row.get('Issue key', '')
        status = row.get('Status', '')
        
        # Try to get description if available
        description = str(row.get('Description', '')) if 'Description' in row else ''
        
        # Search in both summary and description
        text_to_search = summary + ' ' + description
        sti_matches = re.findall(sti_pattern, text_to_search)
        
        for sti in sti_matches:
            all_stis.add(sti)
            # STI code is typically the same as CMDB ID
            cmdb_id = sti
            
            # Add to Excel data
            excel_data.append({
                'STI': sti,
                'CMDB ID': cmdb_id,
                'SOAR Issue Key': key,
                'Status': status,
                'Summary': summary[:200]  # Limit summary length
            })
            
            # Track in map for stats
            if sti not in sti_issue_map:
                sti_issue_map[sti] = []
            sti_issue_map[sti].append({
                'key': key,
                'status': status
            })
        
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1} issues... Found {len(all_stis)} unique STIs", end='\r')
    
    print(f"\n\n✅ Processing complete!")
    print(f"   Total issues processed: {len(df)}")
    print(f"   Unique STIs found: {len(all_stis)}")
    print(f"   Total STI entries (with duplicates): {len(excel_data)}")
    
    # Create DataFrame
    df_excel = pd.DataFrame(excel_data)
    
    # Sort by STI, then by Issue Key
    df_excel = df_excel.sort_values(['STI', 'SOAR Issue Key'])
    
    # Create Excel file
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Main sheet with all entries
        df_excel.to_excel(writer, sheet_name='All STIs', index=False)
        
        # Summary sheet with unique STIs and counts
        sti_summary = []
        for sti in sorted(all_stis):
            issues = sti_issue_map.get(sti, [])
            open_issues = [i for i in issues if i['status'] not in ['Closed', 'Resolved']]
            sti_summary.append({
                'STI': sti,
                'CMDB ID': sti,
                'Total Issues': len(issues),
                'Open Issues': len(open_issues),
                'Closed Issues': len(issues) - len(open_issues)
            })
        
        df_summary = pd.DataFrame(sti_summary)
        df_summary.to_excel(writer, sheet_name='STI Summary', index=False)
        
        # Get worksheets to adjust column widths
        worksheet_all = writer.sheets['All STIs']
        worksheet_summary = writer.sheets['STI Summary']
        
        # Adjust column widths for All STIs sheet
        worksheet_all.column_dimensions['A'].width = 15  # STI
        worksheet_all.column_dimensions['B'].width = 15  # CMDB ID
        worksheet_all.column_dimensions['C'].width = 18  # SOAR Issue Key
        worksheet_all.column_dimensions['D'].width = 20  # Status
        worksheet_all.column_dimensions['E'].width = 80  # Summary
        
        # Adjust column widths for Summary sheet
        worksheet_summary.column_dimensions['A'].width = 15  # STI
        worksheet_summary.column_dimensions['B'].width = 15  # CMDB ID
        worksheet_summary.column_dimensions['C'].width = 15  # Total Issues
        worksheet_summary.column_dimensions['D'].width = 15  # Open Issues
        worksheet_summary.column_dimensions['E'].width = 15  # Closed Issues
    
    print(f"\n✅ Excel file created: {output_file}")
    print(f"   Sheet 1: All STIs - {len(excel_data)} rows")
    print(f"   Sheet 2: STI Summary - {len(all_stis)} unique STIs")
    print(f"\nFirst 10 unique STIs:")
    for sti in sorted(list(all_stis))[:10]:
        count = len(sti_issue_map.get(sti, []))
        print(f"  {sti:<15} - {count:3d} issue(s)")

def main():
    parser = argparse.ArgumentParser(description="Extract all STIs from Jira CSV export")
    parser.add_argument("csv_file", help="Path to Jira CSV export file")
    parser.add_argument("--output", default="SOAR_ALL_STIs_and_CMDB_IDs.xlsx", help="Output Excel file name")
    args = parser.parse_args()
    
    print("="*80)
    print("Extract STIs from Jira CSV Export")
    print("="*80)
    print()
    
    extract_stis_from_csv(args.csv_file, args.output)

if __name__ == "__main__":
    main()




