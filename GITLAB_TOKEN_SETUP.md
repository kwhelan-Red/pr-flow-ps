# How to Create a GitLab Personal Access Token

This guide will help you create a GitLab Personal Access Token (PAT) that can be used to check branch protection rules across all repositories in your organization.

## Step-by-Step Instructions

### For GitLab.com (Cloud)

1. **Log in to GitLab**
   - Go to https://gitlab.com and sign in

2. **Navigate to Access Tokens**
   - Click on your **profile picture/avatar** (top right)
   - Select **Preferences** or **Edit Profile**
   - In the left sidebar, click **Access Tokens**
   - Or go directly to: https://gitlab.com/-/user_settings/personal_access_tokens

3. **Create a New Token**
   - Click **Add new token**
   - Enter a **Token name** (e.g., "Branch Protection Checker" or "API Access")
   - Set an **Expiration date** (optional, but recommended for security)
   - Select the following **scopes**:
     - ✅ **`api`** - Full API access (required)
     - ✅ **`read_api`** - Read-only API access (if you only need to read)
     - ✅ **`read_repository`** - Read repository data (needed to check branch protection)

4. **Generate Token**
   - Click **Create personal access token**
   - **IMPORTANT**: Copy the token immediately! It will only be shown once.
   - The token will look like: `glpat-xxxxxxxxxxxxxxxxxxxx`

5. **Save the Token Securely**
   - Store it in a password manager or secure location
   - You won't be able to see it again after leaving the page

### For Self-Hosted GitLab

1. **Log in to your GitLab instance**
   - Go to your GitLab URL (e.g., `https://gitlab.yourcompany.com`)

2. **Navigate to Access Tokens**
   - Click on your **profile picture/avatar** (top right)
   - Select **Preferences** or **Edit Profile**
   - In the left sidebar, click **Access Tokens**
   - Or go directly to: `https://your-gitlab-instance.com/-/user_settings/personal_access_tokens`

3. **Follow steps 3-5 above** (same as GitLab.com)

## Required Scopes Explained

| Scope | Purpose | Required? |
|-------|---------|-----------|
| **`api`** | Full API access - allows reading and writing via API | ✅ Yes (or use `read_api`) |
| **`read_api`** | Read-only API access - sufficient for checking branch protection | ✅ Yes (alternative to `api`) |
| **`read_repository`** | Read repository data including branches and protection rules | ✅ Recommended |

## Token Format

- GitLab.com tokens start with: `glpat-`
- Self-hosted tokens may vary by version
- Example: `glpat-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Security Best Practices

1. **Set an expiration date** - Don't create tokens that never expire
2. **Use descriptive names** - Name tokens based on their purpose
3. **Limit scope** - Only grant the minimum permissions needed
4. **Rotate regularly** - Create new tokens periodically
5. **Revoke unused tokens** - Delete tokens you no longer need
6. **Never commit tokens** - Don't add tokens to git repositories
7. **Use environment variables** - Store tokens in `.env` files or secure vaults

## Using the Token

Once you have your token, you can use it with the script:

```bash
# Set as environment variable (recommended)
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"

# Or pass directly to script
python check_gitlab_branch_protection.py \
  --url https://gitlab.com \
  --token glpat-xxxxxxxxxxxxxxxxxxxx \
  --group your-group-name
```

## Troubleshooting

### "401 Unauthorized"
- Check that your token is correct
- Verify the token hasn't expired
- Ensure you have the correct scopes

### "403 Forbidden"
- You may not have sufficient permissions on the group/projects
- Try using a token from a user with Maintainer/Owner role
- Check if the group/project is private and you have access

### "404 Not Found"
- Verify the group ID or path is correct
- Check that the GitLab URL is correct
- Ensure the group/project exists and is accessible

## Alternative: Project Access Tokens

If you need to check specific projects, you can also create **Project Access Tokens**:

1. Go to your project
2. Settings → Access Tokens
3. Create token with `read_api` and `read_repository` scopes
4. Note: These are project-specific, not organization-wide

## Group Access Tokens (GitLab Premium/Ultimate)

For organization-level access, you can create **Group Access Tokens**:

1. Go to your group
2. Settings → Access Tokens
3. Create token with appropriate scopes
4. These apply to all projects in the group

---

**Next Steps:**
1. Create your token using the steps above
2. Test it with the script: `python check_gitlab_branch_protection.py --url YOUR_URL --token YOUR_TOKEN --group YOUR_GROUP`

