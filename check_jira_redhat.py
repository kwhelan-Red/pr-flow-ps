#!/usr/bin/env python3
"""
Red Hat Jira API Connection Tool
Uses cookie-based authentication (JSESSIONID) after SSO login
"""

import requests
import sys
from typing import Dict, List, Optional

class RedHatJiraConnector:
    def __init__(self, jira_url: str, jsessionid: str):
        """
        Initialize the Red Hat Jira API client using cookie-based auth
        
        Args:
            jira_url: Jira instance URL (https://issues.redhat.com)
            jsessionid: JSESSIONID cookie value from browser after SSO login
        """
        self.jira_url = jira_url.rstrip('/')
        # Red Hat Jira works better with API v2
        self.api_url = f"{self.jira_url}/rest/api/2"
        self.session = requests.Session()
        
        # Set the JSESSIONID cookie with proper domain and path
        self.session.cookies.set('JSESSIONID', jsessionid, domain='issues.redhat.com', path='/')
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://issues.redhat.com/',
            'Origin': 'https://issues.redhat.com'
        })
    
    def test_connection(self) -> Dict:
        """Test connection to Jira and return user info"""
        try:
            # Try API v2 first (works better with Red Hat Jira)
            response = self.session.get(f"{self.jira_url}/rest/api/2/myself")
            if response.status_code == 200:
                return {
                    'success': True,
                    'user': response.json(),
                    'message': 'Successfully connected to Red Hat Jira'
                }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}',
                    'message': f'Failed to connect: {response.status_code}',
                    'response': response.text[:200]
                }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Failed to connect to Jira: {e}'
            }
    
    def get_projects(self) -> List[Dict]:
        """Get all projects accessible to the user"""
        try:
            response = self.session.get(f"{self.api_url}/project")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching projects: {e}", file=sys.stderr)
            return []
    
    def search_issues(self, jql: str, max_results: int = 50) -> List[Dict]:
        """Search for issues using JQL"""
        try:
            url = f"{self.api_url}/search"
            params = {
                'jql': jql,
                'maxResults': max_results,
                'fields': 'summary,status,assignee,created,updated,priority,issuetype'
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('issues', [])
        except requests.exceptions.RequestException as e:
            print(f"Error searching issues: {e}", file=sys.stderr)
            return []


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Connect to Red Hat Jira using cookie-based authentication'
    )
    parser.add_argument('--url', default='https://issues.redhat.com', help='Jira URL')
    parser.add_argument('--cookie', required=True, help='JSESSIONID cookie value from browser')
    parser.add_argument('--test', action='store_true', help='Test connection only')
    parser.add_argument('--projects', action='store_true', help='List all projects')
    parser.add_argument('--search', help='Search issues using JQL query')
    
    args = parser.parse_args()
    
    # Initialize connector
    jira = RedHatJiraConnector(
        jira_url=args.url,
        jsessionid=args.cookie
    )
    
    # Test connection
    print("Testing Red Hat Jira connection...")
    connection = jira.test_connection()
    if not connection['success']:
        print(f"❌ {connection['message']}")
        if 'response' in connection:
            print(f"Response: {connection['response']}")
        print("\n⚠️  Red Hat Jira requires SSO authentication.")
        print("Please:")
        print("1. Log into https://issues.redhat.com in your browser")
        print("2. Open Developer Tools (F12)")
        print("3. Go to Application → Cookies → issues.redhat.com")
        print("4. Copy the JSESSIONID cookie value")
        sys.exit(1)
    
    user_info = connection['user']
    print(f"✅ Connected to Red Hat Jira")
    print(f"   User: {user_info.get('displayName', 'N/A')}")
    print(f"   Email: {user_info.get('emailAddress', 'N/A')}")
    print(f"   Account ID: {user_info.get('accountId', 'N/A')}\n")
    
    if args.test:
        sys.exit(0)
    
    # List projects
    if args.projects:
        print("Fetching projects...")
        projects = jira.get_projects()
        print(f"\nFound {len(projects)} projects:\n")
        for project in projects[:20]:  # Show first 20
            print(f"  • {project.get('key', 'N/A'):<15} {project.get('name', 'N/A'):<50}")
    
    # Search issues
    if args.search:
        print(f"\nSearching issues with JQL: {args.search}")
        issues = jira.search_issues(args.search)
        print(f"\nFound {len(issues)} issues:\n")
        for issue in issues:
            key = issue.get('key', 'N/A')
            fields = issue.get('fields', {})
            summary = fields.get('summary', 'N/A')[:60]
            status = fields.get('status', {}).get('name', 'N/A')
            print(f"  • {key:<15} {status:<20} {summary}")


if __name__ == '__main__':
    main()

