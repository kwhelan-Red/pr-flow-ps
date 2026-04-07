# Red Hat Jira (issues.redhat.com) API Setup Guide

Red Hat's Jira instance uses different authentication methods than standard Jira Cloud. Here's how to connect.

## Current Issue

The authentication is failing because:
- Red Hat Jira uses **OAuth** authentication
- It requires **CAPTCHA challenge** after failed login attempts
- The token format might be different from standard Jira Cloud tokens

## Solution Options

### Option 1: Get JSESSIONID Cookie (Easiest)

1. **Log into Jira via Browser**
   - Go to https://issues.redhat.com
   - Log in with your Red Hat SSO credentials

2. **Extract JSESSIONID Cookie**
   - Open Developer Tools (F12 or Cmd+Option+I)
   - Go to **Application** tab (Chrome) or **Storage** tab (Firefox)
   - Click on **Cookies** → `https://issues.redhat.com`
   - Find the `JSESSIONID` cookie
   - Copy the entire value (it's a long string)

3. **Use the Cookie**
   ```bash
   python3 check_jira_cookie.py https://issues.redhat.com YOUR_JSESSIONID_VALUE
   ```

### Option 2: Create Personal Access Token

1. **Log into Jira**
   - Go to https://issues.redhat.com
   - Log in with your credentials

2. **Navigate to API Tokens**
   - Click your profile picture (top right)
   - Go to **Account Settings** or **Profile**
   - Look for **Security** or **API Tokens** section
   - Or try: https://issues.redhat.com/secure/ViewProfile.jspa

3. **Create Token**
   - Click **Create API Token** or **Generate Token**
   - Give it a name (e.g., "API Access")
   - Copy the token

4. **Use with Script**
   ```bash
   python3 check_jira.py \
     --url https://issues.redhat.com \
     --email rh-ee-kwhelan \
     --token YOUR_NEW_TOKEN
   ```

### Option 3: Use OAuth 2.0 (Advanced)

Red Hat Jira might require OAuth 2.0 authentication. This requires:
- OAuth client ID and secret
- Authorization flow
- More complex setup

## Quick Test

### Using Cookie Method:

1. **Get Cookie from Browser:**
   - Log into https://issues.redhat.com
   - Open DevTools → Application → Cookies
   - Copy `JSESSIONID` value

2. **Test Connection:**
   ```bash
   python3 check_jira_cookie.py https://issues.redhat.com YOUR_JSESSIONID
   ```

### Using Token Method:

If you create a new Personal Access Token:
```bash
python3 check_jira.py \
  --url https://issues.redhat.com \
  --email rh-ee-kwhelan \
  --token YOUR_TOKEN \
  --test
```

## Finding Your Cookie in Browser

### Chrome/Edge:
1. Press F12 (or Cmd+Option+I on Mac)
2. Go to **Application** tab
3. Left sidebar: **Cookies** → `https://issues.redhat.com`
4. Find `JSESSIONID` in the list
5. Copy the **Value** column

### Firefox:
1. Press F12 (or Cmd+Option+I on Mac)
2. Go to **Storage** tab
3. Left sidebar: **Cookies** → `https://issues.redhat.com`
4. Find `JSESSIONID`
5. Copy the value

### Safari:
1. Enable Developer menu: Preferences → Advanced → Show Develop menu
2. Develop → Show Web Inspector
3. Storage → Cookies → `https://issues.redhat.com`
4. Find `JSESSIONID` and copy value

## Troubleshooting

### "401 Unauthorized"
- Cookie might have expired (log in again and get a new one)
- Token might be incorrect
- Try creating a new token

### "403 Forbidden"
- Your account might not have API access
- Check with your Jira administrator
- Try using a different account with higher permissions

### "CAPTCHA Challenge"
- Too many failed login attempts
- Wait a few minutes and try again
- Use cookie-based authentication instead

## Next Steps

Once authenticated, you can:
- List all projects: `--projects`
- Search issues: `--search "project = PROJ AND status = Open"`
- Get project details: `--project PROJ-KEY`
- List boards: `--boards`

## Security Note

⚠️ **Important**: 
- JSESSIONID cookies expire when you log out
- Don't share cookies or tokens
- Store them securely (use environment variables)
- Rotate tokens regularly

---

**Recommended**: Use the cookie method for quick testing, then set up a Personal Access Token for production use.




