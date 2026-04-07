#!/usr/bin/env python3
"""
GitHub Branch Protection Rules Checker
Fetches branch protection rules for a GitHub repository
"""

import requests
import json
import sys
import argparse
from typing import Dict, Optional
from urllib.parse import urlparse

class GitHubBranchProtectionChecker:
    def __init__(self, token: Optional[str] = None):
        """
        Initialize the GitHub API client
        
        Args:
            token: GitHub personal access token (optional, but recommended for private repos and rate limits)
        """
        self.api_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Branch-Protection-Checker'
        }
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def parse_repo_url(self, repo_url: str) -> tuple:
        """Parse GitHub repository URL to get owner and repo name"""
        # Handle various URL formats
        if 'github.com' not in repo_url:
            raise ValueError("Invalid GitHub URL")
        
        # Parse as URL
        if not repo_url.startswith('http'):
            repo_url = f"https://{repo_url}"
        
        parsed = urlparse(repo_url)
        path = parsed.path.lstrip('/')
        
        # Remove .git suffix if present
        path = path.rstrip('.git')
        
        # Split into owner and repo
        parts = [p for p in path.split('/') if p]  # Remove empty parts
        if len(parts) >= 2:
            owner = parts[0]
            repo = parts[1]
            return owner, repo
        else:
            raise ValueError(f"Could not parse repository from URL: {repo_url}. Got parts: {parts}")
    
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """Get repository information"""
        url = f"{self.api_url}/repos/{owner}/{repo}"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repository info: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 404:
                    print(f"Repository {owner}/{repo} not found or not accessible", file=sys.stderr)
                elif e.response.status_code == 401:
                    print(f"Authentication required. Please provide a GitHub token.", file=sys.stderr)
            raise
    
    def get_branch_protection(self, owner: str, repo: str, branch: str) -> Optional[Dict]:
        """Get branch protection rules for a specific branch"""
        url = f"{self.api_url}/repos/{owner}/{repo}/branches/{branch}/protection"
        try:
            response = self.session.get(url)
            if response.status_code == 404:
                # Branch not protected
                return None
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                if e.response.status_code == 404:
                    return None  # Branch not protected or doesn't exist
                elif e.response.status_code == 403:
                    print(f"Access denied. Token may need 'repo' scope for private repos.", file=sys.stderr)
            print(f"Error fetching branch protection: {e}", file=sys.stderr)
            return None
    
    def get_all_branches(self, owner: str, repo: str) -> list:
        """Get all branches for the repository"""
        url = f"{self.api_url}/repos/{owner}/{repo}/branches"
        branches = []
        page = 1
        per_page = 100
        
        while True:
            params = {'page': page, 'per_page': per_page}
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                page_branches = response.json()
                
                if not page_branches:
                    break
                
                branches.extend([b['name'] for b in page_branches])
                
                if len(page_branches) < per_page:
                    break
                
                page += 1
            except requests.exceptions.RequestException as e:
                print(f"Error fetching branches: {e}", file=sys.stderr)
                break
        
        return branches
    
    def check_repo(self, repo_url: str) -> Dict:
        """Check branch protection for a repository"""
        print(f"Checking repository: {repo_url}\n")
        
        # Parse repository URL
        owner, repo = self.parse_repo_url(repo_url)
        print(f"Repository: {owner}/{repo}\n")
        
        # Get repository info
        try:
            repo_info = self.get_repo_info(owner, repo)
            default_branch = repo_info.get('default_branch', 'main')
            is_private = repo_info.get('private', False)
            print(f"Default branch: {default_branch}")
            print(f"Private: {is_private}\n")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Get branch protection for default branch
        print(f"Checking protection for default branch: {default_branch}...")
        protection = self.get_branch_protection(owner, repo, default_branch)
        
        results = {
            'repository': f"{owner}/{repo}",
            'repository_url': repo_url,
            'default_branch': default_branch,
            'is_private': is_private,
            'default_branch_protected': protection is not None and 'error' not in protection if protection else False,
            'protection_rules': protection,
            'all_branches': []
        }
        
        if protection:
            if 'error' in protection:
                print(f"⚠️  {protection.get('message', 'Authentication required to view protection rules')}\n")
            else:
                print(f"✅ Branch '{default_branch}' is protected\n")
        else:
            print(f"⚠️  Branch '{default_branch}' is NOT protected\n")
        
        # Optionally check other branches
        print("Checking other branches...")
        all_branches = self.get_all_branches(owner, repo)
        results['all_branches'] = all_branches
        
        protected_branches = []
        for branch in all_branches[:10]:  # Limit to first 10 branches to avoid rate limits
            if branch != default_branch:
                branch_protection = self.get_branch_protection(owner, repo, branch)
                if branch_protection:
                    protected_branches.append({
                        'branch': branch,
                        'protection': branch_protection
                    })
        
        results['other_protected_branches'] = protected_branches
        
        return results
    
    def format_protection_rules(self, protection: Dict) -> str:
        """Format protection rules in a human-readable way"""
        if not protection:
            return "No protection rules"
        
        rules = []
        
        # Required status checks
        if 'required_status_checks' in protection:
            status_checks = protection['required_status_checks']
            if status_checks:
                rules.append("Required Status Checks:")
                rules.append(f"  - Strict: {status_checks.get('strict', False)}")
                contexts = status_checks.get('contexts', [])
                if contexts:
                    rules.append(f"  - Contexts: {', '.join(contexts)}")
                else:
                    rules.append("  - No specific contexts required")
        
        # Required pull request reviews
        if 'required_pull_request_reviews' in protection:
            pr_reviews = protection['required_pull_request_reviews']
            if pr_reviews:
                rules.append("\nRequired Pull Request Reviews:")
                rules.append(f"  - Required reviewers: {pr_reviews.get('required_approving_review_count', 0)}")
                rules.append(f"  - Dismiss stale reviews: {pr_reviews.get('dismiss_stale_reviews', False)}")
                rules.append(f"  - Require code owner reviews: {pr_reviews.get('require_code_owner_reviews', False)}")
                rules.append(f"  - Require last push approval: {pr_reviews.get('require_last_push_approval', False)}")
        
        # Enforce admins
        if 'enforce_admins' in protection:
            enforce = protection['enforce_admins']
            if enforce:
                rules.append("\nEnforce for Admins:")
                rules.append(f"  - Enabled: {enforce.get('enabled', False)}")
                rules.append(f"  - URL: {enforce.get('url', 'N/A')}")
        
        # Restrictions
        if 'restrictions' in protection:
            restrictions = protection['restrictions']
            if restrictions:
                rules.append("\nRestrictions:")
                users = restrictions.get('users', [])
                teams = restrictions.get('teams', [])
                apps = restrictions.get('apps', [])
                if users:
                    rules.append(f"  - Users: {', '.join([u.get('login', 'N/A') for u in users])}")
                if teams:
                    rules.append(f"  - Teams: {', '.join([t.get('name', 'N/A') for t in teams])}")
                if apps:
                    rules.append(f"  - Apps: {', '.join([a.get('name', 'N/A') for a in apps])}")
                if not users and not teams and not apps:
                    rules.append("  - No restrictions")
        
        # Allow force pushes
        if 'allow_force_pushes' in protection:
            rules.append(f"\nAllow Force Pushes: {protection.get('allow_force_pushes', False)}")
        
        # Allow deletions
        if 'allow_deletions' in protection:
            rules.append(f"Allow Deletions: {protection.get('allow_deletions', False)}")
        
        # Required linear history
        if 'required_linear_history' in protection:
            rules.append(f"Required Linear History: {protection.get('required_linear_history', False)}")
        
        # Allow squash merging
        if 'allow_squash_merge' in protection:
            rules.append(f"Allow Squash Merge: {protection.get('allow_squash_merge', True)}")
        
        # Allow merge commits
        if 'allow_merge_commits' in protection:
            rules.append(f"Allow Merge Commits: {protection.get('allow_merge_commits', True)}")
        
        # Allow rebase merging
        if 'allow_rebase_merge' in protection:
            rules.append(f"Allow Rebase Merge: {protection.get('allow_rebase_merge', True)}")
        
        # Lock branch
        if 'lock_branch' in protection:
            rules.append(f"Lock Branch: {protection.get('lock_branch', False)}")
        
        return "\n".join(rules) if rules else "No specific rules configured"


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Check branch protection rules for a GitHub repository'
    )
    parser.add_argument('repo_url', help='GitHub repository URL (e.g., https://github.com/owner/repo)')
    parser.add_argument('--token', help='GitHub personal access token (optional but recommended)')
    parser.add_argument('--output', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--file', help='Save output to file')
    
    args = parser.parse_args()
    
    # Initialize checker
    checker = GitHubBranchProtectionChecker(token=args.token)
    
    # Check repository
    try:
        results = checker.check_repo(args.repo_url)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Format output
    if args.output == 'json':
        output = json.dumps(results, indent=2)
    else:
        output = []
        output.append("=" * 80)
        output.append("GITHUB BRANCH PROTECTION REPORT")
        output.append("=" * 80)
        output.append(f"\nRepository: {results['repository']}")
        output.append(f"URL: {results['repository_url']}")
        output.append(f"Default Branch: {results['default_branch']}")
        output.append(f"Private: {results['is_private']}")
        output.append(f"Default Branch Protected: {results['default_branch_protected']}")
        output.append("\n" + "=" * 80)
        
        if results['protection_rules']:
            if 'error' in results['protection_rules']:
                output.append(f"\n⚠️  {results['protection_rules'].get('message', 'Authentication required')}")
                output.append("\nTo view branch protection rules, you need to:")
                output.append("  1. Create a GitHub Personal Access Token")
                output.append("  2. Grant it 'repo' scope (for private repos) or 'public_repo' scope (for public repos)")
                output.append("  3. Run: python3 check_github_branch_protection.py <repo_url> --token <your_token>")
            else:
                output.append("\nPROTECTION RULES:")
                output.append("-" * 80)
                output.append(checker.format_protection_rules(results['protection_rules']))
        else:
            output.append("\n⚠️  No protection rules configured for default branch")
        
        if results['other_protected_branches']:
            output.append("\n\nOTHER PROTECTED BRANCHES:")
            output.append("-" * 80)
            for branch_info in results['other_protected_branches']:
                output.append(f"\nBranch: {branch_info['branch']}")
                output.append(checker.format_protection_rules(branch_info['protection']))
        
        output.append("\n" + "=" * 80)
        output = "\n".join(output)
    
    # Output report
    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"\n✅ Report saved to {args.file}")
    else:
        print("\n" + output)


if __name__ == '__main__':
    main()
