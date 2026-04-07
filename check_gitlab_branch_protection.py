#!/usr/bin/env python3
"""
GitLab Branch Protection Rules Checker
Checks branch protection rules for all repositories in a GitLab group/organization
"""

import requests
import json
import sys
from typing import List, Dict, Optional
from urllib.parse import urljoin

class GitLabBranchProtectionChecker:
    def __init__(self, gitlab_url: str, access_token: str, group_id: Optional[str] = None):
        """
        Initialize the GitLab API client
        
        Args:
            gitlab_url: GitLab instance URL (e.g., 'https://gitlab.com' or 'https://gitlab.example.com')
            access_token: Personal access token or project access token with appropriate permissions
            group_id: Optional group ID or path to check. If None, will check all accessible projects
        """
        self.gitlab_url = gitlab_url.rstrip('/')
        self.api_url = f"{self.gitlab_url}/api/v4"
        self.headers = {
            'PRIVATE-TOKEN': access_token,
            'Content-Type': 'application/json'
        }
        self.group_id = group_id
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_all_projects(self) -> List[Dict]:
        """Get all projects accessible to the token"""
        projects = []
        page = 1
        per_page = 100
        
        while True:
            if self.group_id:
                url = f"{self.api_url}/groups/{self.group_id}/projects"
            else:
                url = f"{self.api_url}/projects"
            
            params = {
                'page': page,
                'per_page': per_page,
                'simple': False,
                'membership': True  # Only projects user is a member of
            }
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                page_projects = response.json()
                
                if not page_projects:
                    break
                
                projects.extend(page_projects)
                
                # Check if there are more pages
                if len(page_projects) < per_page:
                    break
                
                page += 1
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching projects: {e}", file=sys.stderr)
                if hasattr(e.response, 'text'):
                    print(f"Response: {e.response.text}", file=sys.stderr)
                break
        
        return projects
    
    def get_protected_branches(self, project_id: int) -> List[Dict]:
        """Get protected branches for a specific project"""
        url = f"{self.api_url}/projects/{project_id}/protected_branches"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching protected branches for project {project_id}: {e}", file=sys.stderr)
            return []
    
    def get_group_protected_branches(self, group_id: str) -> List[Dict]:
        """Get group-level protected branches"""
        url = f"{self.api_url}/groups/{group_id}/protected_branches"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Group-level protection might not be available or accessible
            return []
    
    def check_all_repos(self) -> Dict:
        """Check branch protection for all repositories"""
        print("Fetching all projects...")
        projects = self.get_all_projects()
        print(f"Found {len(projects)} projects\n")
        
        results = {
            'total_projects': len(projects),
            'projects_with_protection': 0,
            'projects_without_protection': 0,
            'projects': []
        }
        
        for project in projects:
            project_id = project['id']
            project_name = project['name']
            project_path = project['path_with_namespace']
            default_branch = project.get('default_branch', 'N/A')
            
            print(f"Checking {project_path}...", end=' ')
            
            protected_branches = self.get_protected_branches(project_id)
            
            project_result = {
                'id': project_id,
                'name': project_name,
                'path': project_path,
                'default_branch': default_branch,
                'protected_branches': protected_branches,
                'has_protection': len(protected_branches) > 0,
                'default_branch_protected': False
            }
            
            # Check if default branch is protected
            if default_branch != 'N/A':
                for pb in protected_branches:
                    if pb.get('name') == default_branch or pb.get('name') == '*' or default_branch.startswith(pb.get('name', '').rstrip('*')):
                        project_result['default_branch_protected'] = True
                        break
            
            if project_result['has_protection']:
                results['projects_with_protection'] += 1
            else:
                results['projects_without_protection'] += 1
            
            results['projects'].append(project_result)
            print(f"{'✓' if project_result['has_protection'] else '✗'}")
        
        # Check group-level protections if group_id is provided
        if self.group_id:
            print(f"\nChecking group-level protections for group {self.group_id}...")
            group_protections = self.get_group_protected_branches(self.group_id)
            results['group_protections'] = group_protections
        
        return results
    
    def generate_report(self, results: Dict, output_format: str = 'table') -> str:
        """Generate a human-readable report"""
        if output_format == 'table':
            return self._generate_table_report(results)
        elif output_format == 'json':
            return json.dumps(results, indent=2)
        else:
            return self._generate_text_report(results)
    
    def _generate_table_report(self, results: Dict) -> str:
        """Generate a table-formatted report"""
        report = []
        report.append("=" * 120)
        report.append("GITLAB BRANCH PROTECTION REPORT")
        report.append("=" * 120)
        report.append(f"\nTotal Projects: {results['total_projects']}")
        report.append(f"Projects with Protection: {results['projects_with_protection']}")
        report.append(f"Projects without Protection: {results['projects_without_protection']}")
        report.append("\n" + "=" * 120)
        report.append("\nDetailed Results:\n")
        
        # Table header
        report.append(f"{'Project Path':<50} {'Default Branch':<20} {'Protected?':<12} {'Protection Rules':<30}")
        report.append("-" * 120)
        
        for project in results['projects']:
            path = project['path'][:48]
            default = project['default_branch'][:18]
            protected = "✓ Yes" if project['has_protection'] else "✗ No"
            
            protection_rules = []
            for pb in project['protected_branches']:
                rule = pb.get('name', 'N/A')
                push_level = pb.get('push_access_levels', [{}])[0].get('access_level_description', 'N/A')
                merge_level = pb.get('merge_access_levels', [{}])[0].get('access_level_description', 'N/A')
                protection_rules.append(f"{rule} (push:{push_level}, merge:{merge_level})")
            
            rules_str = "; ".join(protection_rules[:2])[:28] if protection_rules else "None"
            
            report.append(f"{path:<50} {default:<20} {protected:<12} {rules_str:<30}")
        
        return "\n".join(report)
    
    def _generate_text_report(self, results: Dict) -> str:
        """Generate a text-formatted report"""
        report = []
        report.append("GITLAB BRANCH PROTECTION REPORT")
        report.append("=" * 80)
        report.append(f"\nTotal Projects: {results['total_projects']}")
        report.append(f"Projects with Protection: {results['projects_with_protection']}")
        report.append(f"Projects without Protection: {results['projects_without_protection']}")
        report.append("\n" + "=" * 80)
        
        for project in results['projects']:
            report.append(f"\nProject: {project['path']}")
            report.append(f"  Default Branch: {project['default_branch']}")
            report.append(f"  Has Protection: {project['has_protection']}")
            report.append(f"  Default Branch Protected: {project['default_branch_protected']}")
            
            if project['protected_branches']:
                report.append("  Protected Branches:")
                for pb in project['protected_branches']:
                    report.append(f"    - {pb.get('name', 'N/A')}")
                    report.append(f"      Push Access: {pb.get('push_access_levels', [{}])[0].get('access_level_description', 'N/A')}")
                    report.append(f"      Merge Access: {pb.get('merge_access_levels', [{}])[0].get('access_level_description', 'N/A')}")
            else:
                report.append("  No protected branches configured")
        
        return "\n".join(report)


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Check branch protection rules for all GitLab repositories in a group/organization'
    )
    parser.add_argument('--url', required=True, help='GitLab instance URL (e.g., https://gitlab.com)')
    parser.add_argument('--token', required=True, help='GitLab personal access token')
    parser.add_argument('--group', help='Group ID or path (optional, checks all accessible projects if not provided)')
    parser.add_argument('--output', choices=['table', 'json', 'text'], default='table', help='Output format')
    parser.add_argument('--file', help='Save output to file')
    
    args = parser.parse_args()
    
    # Initialize checker
    checker = GitLabBranchProtectionChecker(
        gitlab_url=args.url,
        access_token=args.token,
        group_id=args.group
    )
    
    # Check all repositories
    results = checker.check_all_repos()
    
    # Generate report
    report = checker.generate_report(results, output_format=args.output)
    
    # Output report
    if args.file:
        with open(args.file, 'w') as f:
            f.write(report)
        print(f"\nReport saved to {args.file}")
    else:
        print("\n" + report)


if __name__ == '__main__':
    main()

