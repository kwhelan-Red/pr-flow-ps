# How to Connect to Jira API

This guide will help you set up access to Jira's REST API to query projects, issues, and other data.

## Prerequisites

### For Jira Cloud (atlassian.net)

1. **Jira Instance URL**
   - Format: `https://your-domain.atlassian.net`
   - You can find this in your Jira URL when logged in

2. **API Token**
   - Go to: https://id.atlassian.com/manage-profile/security/api-tokens
   - Or: Profile → Security → API tokens
   - Click **Create API token**
   - Give it a name (e.g., "Jira API Access")
   - Copy the token immediately (starts with `ATATT...`)

3. **Email Address**
   - Use the email address associated with your Jira account

### For Jira Server/Data Center

1. **Jira Instance URL**
   - Format: `https://jira.yourcompany.com`
   - Your organization's Jira server URL

2. **Username and Password**
   - Use your Jira username (not email)
   - Use your Jira password (or an app password if 2FA is enabled)

## Installation

```bash
# Install required Python library
pip install requests
# or
pip3 install --break-system-packages requests
```

## Usage Examples

### Test Connection

```bash
python check_jira.py \
  --url https://your-domain.atlassian.net \
  --email your-email@example.com \
  --token YOUR_API_TOKEN \
  --test
```

### List All Projects

```bash
python check_jira.py \
  --url https://your-domain.atlassian.net \
  --email your-email@example.com \
  --token YOUR_API_TOKEN \
  --projects
```

### Get Project Details

```bash
python check_jira.py \
  --url https://your-domain.atlassian.net \
  --email your-email@example.com \
  --token YOUR_API_TOKEN \
  --project PROJ
```

### Search Issues (JQL)

```bash
python check_jira.py \
  --url https://your-domain.atlassian.net \
  --email your-email@example.com \
  --token YOUR_API_TOKEN \
  --search "project = PROJ AND status = Open"
```

### Get Specific Issue

```bash
python check_jira.py \
  --url https://your-domain.atlassian.net \
  --email your-email@example.com \
  --token YOUR_API_TOKEN \
  --issue PROJ-123
```

### List All Boards

```bash
python check_jira.py \
  --url https://your-domain.atlassian.net \
  --email your-email@example.com \
  --token YOUR_API_TOKEN \
  --boards
```

## JQL (Jira Query Language) Examples

JQL is used to search for issues. Here are common examples:

```jql
# All open issues in a project
project = PROJ AND status = Open

# Issues assigned to me
assignee = currentUser()

# High priority issues
priority = High

# Issues created in last 7 days
created >= -7d

# Issues in a specific sprint
sprint = "Sprint 1"

# Issues with specific labels
labels = security

# Complex query
project = PROJ AND status IN (Open, "In Progress") AND priority = High
```

## API Token Creation Steps (Jira Cloud)

1. **Navigate to API Tokens**
   - Go to: https://id.atlassian.com/manage-profile/security/api-tokens
   - Or: Click your profile → Account settings → Security → API tokens

2. **Create Token**
   - Click **Create API token**
   - Enter a label (e.g., "Jira API Script")
   - Click **Create**

3. **Copy Token**
   - Copy the token immediately (format: `ATATT...`)
   - You won't be able to see it again

4. **Store Securely**
   - Save in a password manager
   - Never commit to git repositories
   - Use environment variables when possible

## Security Best Practices

1. **Use API Tokens** - Don't use your password directly
2. **Set Expiration** - Create tokens with expiration dates
3. **Limit Scope** - Only grant necessary permissions
4. **Rotate Regularly** - Create new tokens periodically
5. **Use Environment Variables** - Store tokens securely:
   ```bash
   export JIRA_URL="https://your-domain.atlassian.net"
   export JIRA_EMAIL="your-email@example.com"
   export JIRA_TOKEN="YOUR_TOKEN"
   ```

## Troubleshooting

### "401 Unauthorized"
- Check that your email and API token are correct
- Verify the token hasn't expired
- For Jira Server, ensure username (not email) is used

### "403 Forbidden"
- You may not have permission to access the requested resource
- Check project permissions
- Verify your account has appropriate roles

### "404 Not Found"
- Verify the Jira URL is correct
- Check that the project/issue key exists
- Ensure you have access to the resource

### Connection Timeout
- Check your network connection
- Verify the Jira instance URL is accessible
- For corporate networks, check firewall/proxy settings

## What You Can Do with the API

- ✅ List all projects
- ✅ Get project details
- ✅ Search issues using JQL
- ✅ Get issue details
- ✅ List boards (Scrum/Kanban)
- ✅ Create/update issues (with additional code)
- ✅ Get sprints and backlogs
- ✅ Query workflows and statuses
- ✅ Get user information
- ✅ Retrieve custom fields

## Next Steps

Once connected, you can:
1. Query all projects in your organization
2. Check issue statuses and assignments
3. Generate reports on project health
4. Monitor open issues and blockers
5. Track sprint progress
6. Analyze team velocity

---

**Ready to connect?** Run the test command with your credentials!

