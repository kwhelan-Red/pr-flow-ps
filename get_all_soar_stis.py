#!/usr/bin/env python3
"""
Extract ALL STIs and CMDB IDs from ALL SOAR issues (not just open ones)
Creates an Excel file with all STIs and their associated issues.
"""

import requests
import re
import pandas as pd
import sys
import argparse

def get_all_soar_stis(jira_url, jsessionid):
    """Get all STIs from all SOAR issues"""
    
    session = requests.Session()
    session.cookies.set('JSESSIONID', jsessionid, domain='issues.redhat.com', path='/')
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://issues.redhat.com/',
    })

    # Test connection
    print("Testing connection...")
    try:
        response = session.get(f"{jira_url}/rest/api/2/myself")
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Connected as: {user.get('displayName', 'N/A')}\n")
        else:
            print(f"❌ Connection failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

    # Get ALL SOAR issues
    jql = "project = SOAR"
    api_url = f"{jira_url}/rest/api/2/search"

    all_stis = set()
    sti_issue_map = {}
    excel_data = []

    print("Fetching ALL SOAR issues to extract all STIs...\n")

    start_at = 0
    max_results = 100
    total_processed = 0

    sti_pattern = r'\[([A-Z0-9]+-[0-9]+)\]'

    while True:
        params = {
            'jql': jql,
            'startAt': start_at,
            'maxResults': max_results,
            'fields': 'key,summary,status',
        }
        
        try:
            response = session.get(api_url, params=params)
            if response.status_code == 401:
                print("\n❌ Authentication failed - cookie may have expired")
                return None
            response.raise_for_status()
            data = response.json()
            
            issues = data.get('issues', [])
            if not issues:
                break
            
            total = data.get('total', 0)
            
            for issue in issues:
                key = issue.get('key', '')
                summary = issue.get('fields', {}).get('summary', '')
                status = issue.get('fields', {}).get('status', {}).get('name', '')
                
                sti_matches = re.findall(sti_pattern, summary)
                
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
            
            total_processed += len(issues)
            start_at += len(issues)
            
            print(f"Processed {total_processed} of {total} issues... Found {len(all_stis)} unique STIs, {len(excel_data)} total entries", end='\r')
            
            if start_at >= total:
                break
                
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
            return None

    print(f"\n\n✅ Processing complete!")
    print(f"   Total issues processed: {total_processed}")
    print(f"   Unique STIs found: {len(all_stis)}")
    print(f"   Total STI entries (with duplicates): {len(excel_data)}")

    # Create DataFrame
    df_excel = pd.DataFrame(excel_data)

    # Sort by STI, then by Issue Key
    df_excel = df_excel.sort_values(['STI', 'SOAR Issue Key'])

    return {
        'all_data': df_excel,
        'unique_stis': all_stis,
        'sti_issue_map': sti_issue_map
    }

def create_excel_file(data, output_file):
    """Create Excel file with all STI data"""
    
    df_excel = data['all_data']
    all_stis = data['unique_stis']
    sti_issue_map = data['sti_issue_map']
    
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

def main():
    parser = argparse.ArgumentParser(description="Extract all STIs from all SOAR issues")
    parser.add_argument("--cookie", required=True, help="JSESSIONID cookie value")
    parser.add_argument("--output", default="SOAR_ALL_STIs_and_CMDB_IDs.xlsx", help="Output Excel file name")
    args = parser.parse_args()

    jira_url = "https://issues.redhat.com"
    
    print("="*80)
    print("SOAR - Extract ALL STIs and CMDB IDs")
    print("="*80)
    print()
    
    # Get all STI data
    data = get_all_soar_stis(jira_url, args.cookie)
    
    if data is None:
        print("\n❌ Failed to retrieve data. Check your JSESSIONID cookie.")
        sys.exit(1)
    
    # Create Excel file
    output_file = args.output
    create_excel_file(data, output_file)
    
    print(f"\n✅ Excel file created: {output_file}")
    print(f"   Sheet 1: All STIs - {len(data['all_data'])} rows (includes duplicates if STI appears in multiple issues)")
    print(f"   Sheet 2: STI Summary - {len(data['unique_stis'])} unique STIs with counts")
    print(f"\nFirst 10 unique STIs:")
    for sti in sorted(list(data['unique_stis']))[:10]:
        count = len(data['sti_issue_map'].get(sti, []))
        print(f"  {sti:<15} - {count:3d} issue(s)")

if __name__ == "__main__":
    main()




