#!/usr/bin/env python3
"""
Get SOA (Security Operating Approval) approval status for SOAR project issues
"""

import requests
import sys
from typing import Dict, List

def get_soar_issues(jira_url: str, jsessionid: str) -> List[Dict]:
    """Get all open issues from SOAR project"""
    session = requests.Session()
    session.cookies.set('JSESSIONID', jsessionid, domain='issues.redhat.com', path='/')
    session.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://issues.redhat.com/',
    })
    
    # Search for all open issues in SOAR project
    jql = "project = SOAR AND status != Closed AND status != Resolved"
    api_url = f"{jira_url}/rest/api/2/search"
    
    all_issues = []
    start_at = 0
    max_results = 100
    
    while True:
        params = {
            'jql': jql,
            'startAt': start_at,
            'maxResults': max_results,
            'fields': '*all',  # Get all fields to find SOA-related ones
            'expand': 'fields'
        }
        
        try:
            response = session.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            issues = data.get('issues', [])
            if not issues:
                break
            
            all_issues.extend(issues)
            
            # Check if there are more results
            total = data.get('total', 0)
            start_at += len(issues)
            
            if start_at >= total:
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issues: {e}", file=sys.stderr)
            break
    
    return all_issues


def find_soa_field(issue: Dict) -> tuple:
    """Find SOA approval status field in issue"""
    fields = issue.get('fields', {})
    
    # Common field names for SOA approval
    soa_keywords = ['soa', 'security operating approval', 'operating approval', 'approval status']
    
    soa_field_name = None
    soa_value = None
    
    # Search through all fields
    for key, value in fields.items():
        key_lower = str(key).lower()
        value_str = str(value).lower() if value else ""
        
        # Check if field name or value contains SOA-related terms
        if any(keyword in key_lower for keyword in soa_keywords):
            soa_field_name = key
            soa_value = value
            break
        elif value and any(keyword in value_str for keyword in soa_keywords):
            # Check if it's a custom field with SOA in the value
            if 'customfield' in key_lower:
                soa_field_name = key
                soa_value = value
                break
    
    return soa_field_name, soa_value


def categorize_issues(issues: List[Dict]) -> Dict:
    """Categorize issues by SOA approval status"""
    approved = []
    not_approved = []
    unknown = []
    
    for issue in issues:
        key = issue.get('key', 'N/A')
        summary = issue.get('fields', {}).get('summary', 'N/A')
        status = issue.get('fields', {}).get('status', {}).get('name', 'N/A')
        
        soa_field, soa_value = find_soa_field(issue)
        
        issue_info = {
            'key': key,
            'summary': summary,
            'status': status,
            'soa_field': soa_field,
            'soa_value': soa_value
        }
        
        if soa_value:
            soa_str = str(soa_value).lower()
            if any(term in soa_str for term in ['approved', 'yes', 'true', 'complete', 'done']):
                approved.append(issue_info)
            elif any(term in soa_str for term in ['not approved', 'no', 'false', 'pending', 'rejected']):
                not_approved.append(issue_info)
            else:
                unknown.append(issue_info)
        else:
            unknown.append(issue_info)
    
    return {
        'approved': approved,
        'not_approved': not_approved,
        'unknown': unknown
    }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Get SOA approval status for SOAR project issues'
    )
    parser.add_argument('--cookie', required=True, help='JSESSIONID cookie value')
    parser.add_argument('--url', default='https://issues.redhat.com', help='Jira URL')
    parser.add_argument('--output', choices=['table', 'json'], default='table', help='Output format')
    
    args = parser.parse_args()
    
    print("Fetching SOAR project issues...")
    issues = get_soar_issues(args.url, args.cookie)
    
    if not issues:
        print("No issues found or error occurred.")
        sys.exit(1)
    
    print(f"Found {len(issues)} open issues\n")
    print("Analyzing SOA approval status...\n")
    
    categorized = categorize_issues(issues)
    
    if args.output == 'json':
        import json
        print(json.dumps(categorized, indent=2))
    else:
        # Table format
        print("="*100)
        print("SOA APPROVED ISSUES")
        print("="*100)
        if categorized['approved']:
            print(f"\nTotal: {len(categorized['approved'])}\n")
            for issue in categorized['approved']:
                print(f"{issue['key']:<15} {issue['status']:<20} {issue['summary'][:60]}")
                if issue['soa_field']:
                    print(f"  SOA Field: {issue['soa_field']} = {issue['soa_value']}")
        else:
            print("\nNo approved issues found")
        
        print("\n" + "="*100)
        print("SOA NOT APPROVED / PENDING ISSUES")
        print("="*100)
        if categorized['not_approved']:
            print(f"\nTotal: {len(categorized['not_approved'])}\n")
            for issue in categorized['not_approved']:
                print(f"{issue['key']:<15} {issue['status']:<20} {issue['summary'][:60]}")
                if issue['soa_field']:
                    print(f"  SOA Field: {issue['soa_field']} = {issue['soa_value']}")
        else:
            print("\nNo not-approved issues found")
        
        print("\n" + "="*100)
        print("ISSUES WITH UNKNOWN SOA STATUS")
        print("="*100)
        if categorized['unknown']:
            print(f"\nTotal: {len(categorized['unknown'])}\n")
            print("(These issues may not have SOA field set or field name is unknown)\n")
            for issue in categorized['unknown'][:20]:  # Show first 20
                print(f"{issue['key']:<15} {issue['status']:<20} {issue['summary'][:60]}")
            if len(categorized['unknown']) > 20:
                print(f"\n... and {len(categorized['unknown']) - 20} more")
        
        print("\n" + "="*100)
        print("SUMMARY")
        print("="*100)
        print(f"SOA Approved:        {len(categorized['approved'])}")
        print(f"SOA Not Approved:    {len(categorized['not_approved'])}")
        print(f"Unknown Status:      {len(categorized['unknown'])}")
        print(f"Total Issues:        {len(issues)}")


if __name__ == '__main__':
    main()




