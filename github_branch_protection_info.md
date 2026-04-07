# GitHub Branch Protection Rules - ansible-role-rhel8-stig

**Repository:** [RedHatOfficial/ansible-role-rhel8-stig](https://github.com/RedHatOfficial/ansible-role-rhel8-stig)

## Repository Information

- **Owner:** RedHatOfficial
- **Repository:** ansible-role-rhel8-stig
- **Default Branch:** master
- **Visibility:** Public
- **Description:** DISA STIG for Red Hat Enterprise Linux 8 - Ansible role generated from ComplianceAsCode Project

## Branch Protection Rules

⚠️ **Authentication Required**

GitHub's API requires authentication to view branch protection rules, even for public repositories. The branch protection endpoint (`/repos/{owner}/{repo}/branches/{branch}/protection`) returns a 401 Unauthorized response without authentication.

### How to Get Branch Protection Rules

#### Option 1: Using GitHub Personal Access Token

1. **Create a Personal Access Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: "Branch Protection Checker"
   - Select scope: `public_repo` (for public repos) or `repo` (for private repos)
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again)

2. **Run the script with token:**
   ```bash
   python3 check_github_branch_protection.py \
     "https://github.com/RedHatOfficial/ansible-role-rhel8-stig" \
     --token YOUR_GITHUB_TOKEN
   ```

#### Option 2: Manual Check via GitHub Web Interface

1. Navigate to: https://github.com/RedHatOfficial/ansible-role-rhel8-stig
2. Go to **Settings** → **Branches**
3. View branch protection rules configured for the repository

#### Option 3: Using GitHub CLI (gh)

If you have GitHub CLI installed:

```bash
gh api repos/RedHatOfficial/ansible-role-rhel8-stig/branches/master/protection
```

## Script Usage

The script `check_github_branch_protection.py` can check branch protection rules:

```bash
# Without token (will show authentication required message)
python3 check_github_branch_protection.py "https://github.com/RedHatOfficial/ansible-role-rhel8-stig"

# With token (will show actual protection rules)
python3 check_github_branch_protection.py \
  "https://github.com/RedHatOfficial/ansible-role-rhel8-stig" \
  --token ghp_xxxxxxxxxxxx

# Save to file
python3 check_github_branch_protection.py \
  "https://github.com/RedHatOfficial/ansible-role-rhel8-stig" \
  --token YOUR_TOKEN \
  --file branch_protection_report.txt

# JSON output
python3 check_github_branch_protection.py \
  "https://github.com/RedHatOfficial/ansible-role-rhel8-stig" \
  --token YOUR_TOKEN \
  --output json
```

## What the Script Checks

- Default branch protection status
- Required status checks
- Required pull request reviews
- Required number of approvals
- Dismiss stale reviews
- Require code owner reviews
- Enforce admins
- Branch restrictions (users/teams)
- Allow force pushes
- Allow deletions
- Required linear history
- Merge options (squash, merge, rebase)
- Lock branch

## Notes

- Public repositories still require authentication to view branch protection rules via API
- The `public_repo` scope is sufficient for public repositories
- For private repositories, you need the `repo` scope
- Rate limits apply: 60 requests/hour without authentication, 5,000 requests/hour with authentication
