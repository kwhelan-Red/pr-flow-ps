#!/usr/bin/env python3
"""
Jira API Connection and Query Tool
Connects to Jira and retrieves information about projects, issues, and more
"""

import requests
import json
import sys
from typing import Dict, List, Optional
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin

class JiraConnector:
    def __init__(self, jira_url: str, email: str, api_token: str, use_oauth: bool = False):
        """
        Initialize the Jira API client
        
        Args:
            jira_url: Jira instance URL (e.g., 'https://your-domain.atlassian.net' or 'https://jira.example.com')
            email: Your Jira email address (for Jira Cloud) or username (for Jira Server)
            api_token: Jira API token (for Jira Cloud) or password (for Jira Server)
            use_oauth: If True, attempt OAuth authentication (for some Jira Server instances)
        """
        self.jira_url = jira_url.rstrip('/')
        self.api_url = f"{self.jira_url}/rest/api/3"
        self.email = email
        self.api_token = api_token
        self.use_oauth = use_oauth
        
        self.session = requests.Session()
        
        # Try different authentication methods
        if use_oauth:
            # For OAuth, we might need to get a session token first
            # This is a placeholder - actual OAuth flow is more complex
            self.session.headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_token}'  # Try Bearer token
            })
        else:
            # Use Basic Auth with email and API token for Jira Cloud
            # For Jira Server, use username and password
            self.auth = HTTPBasicAuth(email, api_token)
            self.session.auth = self.auth
            self.session.headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            })
    
    def test_connection(self) -> Dict:
        """Test connection to Jira and return user info"""
        try:
            response = self.session.get(f"{self.api_url}/myself")
            response.raise_for_status()
            return {
                'success': True,
                'user': response.json(),
                'message': 'Successfully connected to Jira'
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
    
    def get_project(self, project_key: str) -> Optional[Dict]:
        """Get details for a specific project"""
        try:
            response = self.session.get(f"{self.api_url}/project/{project_key}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching project {project_key}: {e}", file=sys.stderr)
            return None
    
    def search_issues(self, jql: str, max_results: int = 50) -> List[Dict]:
        """
        Search for issues using JQL (Jira Query Language)
        
        Args:
            jql: JQL query string (e.g., 'project = PROJ AND status = Open')
            max_results: Maximum number of results to return
        """
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
    
    def get_issue(self, issue_key: str) -> Optional[Dict]:
        """Get details for a specific issue"""
        try:
            response = self.session.get(f"{self.api_url}/issue/{issue_key}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching issue {issue_key}: {e}", file=sys.stderr)
            return None
    
    def get_project_issues(self, project_key: str, status: Optional[str] = None) -> List[Dict]:
        """Get all issues for a project, optionally filtered by status"""
        jql = f"project = {project_key}"
        if status:
            jql += f" AND status = {status}"
        return self.search_issues(jql)
    
    def get_boards(self, project_key: Optional[str] = None) -> List[Dict]:
        """Get all boards (Scrum/Kanban boards)"""
        try:
            url = f"{self.jira_url}/rest/agile/1.0/board"
            params = {}
            if project_key:
                params['projectKeyOrId'] = project_key
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('values', [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching boards: {e}", file=sys.stderr)
            return []


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Connect to Jira and retrieve information'
    )
    parser.add_argument('--url', required=True, help='Jira instance URL (e.g., https://your-domain.atlassian.net)')
    parser.add_argument('--email', required=True, help='Your Jira email address (for Cloud) or username (for Server)')
    parser.add_argument('--token', required=True, help='Jira API token (for Cloud) or password (for Server)')
    parser.add_argument('--test', action='store_true', help='Test connection only')
    parser.add_argument('--projects', action='store_true', help='List all projects')
    parser.add_argument('--project', help='Get details for a specific project (project key)')
    parser.add_argument('--search', help='Search issues using JQL query')
    parser.add_argument('--issue', help='Get details for a specific issue (issue key)')
    parser.add_argument('--boards', action='store_true', help='List all boards')
    parser.add_argument('--output', choices=['json', 'table'], default='table', help='Output format')
    
    args = parser.parse_args()
    
    # Initialize connector
    jira = JiraConnector(
        jira_url=args.url,
        email=args.email,
        api_token=args.token
    )
    
    # Test connection
    print("Testing Jira connection...")
    connection = jira.test_connection()
    if not connection['success']:
        print(f"❌ {connection['message']}")
        if 'error' in connection:
            print(f"Error details: {connection['error']}")
        sys.exit(1)
    
    user_info = connection['user']
    print(f"✅ Connected to Jira")
    print(f"   User: {user_info.get('displayName', 'N/A')} ({user_info.get('emailAddress', 'N/A')})")
    print(f"   Account ID: {user_info.get('accountId', 'N/A')}\n")
    
    if args.test:
        sys.exit(0)
    
    # List projects
    if args.projects:
        print("Fetching projects...")
        projects = jira.get_projects()
        print(f"\nFound {len(projects)} projects:\n")
        for project in projects:
            print(f"  • {project.get('key', 'N/A'):<15} {project.get('name', 'N/A'):<50} ({project.get('projectTypeKey', 'N/A')})")
    
    # Get specific project
    if args.project:
        print(f"\nFetching project: {args.project}")
        project = jira.get_project(args.project)
        if project:
            print(f"\nProject: {project.get('name', 'N/A')}")
            print(f"Key: {project.get('key', 'N/A')}")
            print(f"Type: {project.get('projectTypeKey', 'N/A')}")
            print(f"Lead: {project.get('lead', {}).get('displayName', 'N/A')}")
    
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
    
    # Get specific issue
    if args.issue:
        print(f"\nFetching issue: {args.issue}")
        issue = jira.get_issue(args.issue)
        if issue:
            fields = issue.get('fields', {})
            print(f"\nIssue: {issue.get('key', 'N/A')}")
            print(f"Summary: {fields.get('summary', 'N/A')}")
            print(f"Status: {fields.get('status', {}).get('name', 'N/A')}")
            print(f"Assignee: {fields.get('assignee', {}).get('displayName', 'Unassigned')}")
            print(f"Priority: {fields.get('priority', {}).get('name', 'N/A')}")
            print(f"Type: {fields.get('issuetype', {}).get('name', 'N/A')}")
    
    # List boards
    if args.boards:
        print("\nFetching boards...")
        boards = jira.get_boards()
        print(f"\nFound {len(boards)} boards:\n")
        for board in boards:
            print(f"  • {board.get('name', 'N/A'):<50} (ID: {board.get('id', 'N/A')}, Type: {board.get('type', 'N/A')})")
    
    # If no specific action, show available projects
    if not any([args.projects, args.project, args.search, args.issue, args.boards]):
        print("\nAvailable actions:")
        print("  --projects          List all projects")
        print("  --project KEY       Get details for a specific project")
        print("  --search 'JQL'      Search issues using JQL")
        print("  --issue KEY         Get details for a specific issue")
        print("  --boards            List all boards")
        print("\nExample:")
        print("  python check_jira.py --url https://your-domain.atlassian.net --email user@example.com --token TOKEN --projects")


if __name__ == '__main__':
    main()

