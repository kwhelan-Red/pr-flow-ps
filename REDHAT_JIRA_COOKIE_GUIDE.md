# Red Hat Jira Authentication Guide

## Issue

Red Hat Jira (`issues.redhat.com`) uses **SAML/SSO authentication** through Red Hat's SSO system. Standard API token authentication (Basic Auth) doesn't work because it redirects to SSO login.

## Solution: Cookie-Based Authentication

Since Red Hat Jira requires SSO, you need to use **cookie-based authentication** with the `JSESSIONID` cookie from your browser session.

## Steps to Get JSESSIONID Cookie

### 1. Log into Jira
- Go to https://issues.redhat.com
- Log in with your Red Hat SSO credentials

### 2. Extract JSESSIONID Cookie

#### Chrome/Edge:
1. Press **F12** (or **Cmd+Option+I** on Mac) to open Developer Tools
2. Go to **Application** tab
3. In left sidebar: **Cookies** → `https://issues.redhat.com`
4. Find `JSESSIONID` in the list
5. Copy the **Value** (it's a long string like `A1B2C3D4E5F6...`)

#### Firefox:
1. Press **F12** (or **Cmd+Option+I** on Mac)
2. Go to **Storage** tab
3. Left sidebar: **Cookies** → `https://issues.redhat.com`
4. Find `JSESSIONID` and copy the value

#### Safari:
1. Enable Developer menu: **Preferences** → **Advanced** → **Show Develop menu**
2. **Develop** → **Show Web Inspector**
3. **Storage** → **Cookies** → `https://issues.redhat.com`
4. Find `JSESSIONID` and copy value

### 3. Use the Cookie

```bash
python3 check_jira_redhat.py \
  --cookie YOUR_JSESSIONID_VALUE \
  --test
```

## Example Usage

### Test Connection
```bash
python3 check_jira_redhat.py \
  --cookie A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6 \
  --test
```

### List Projects
```bash
python3 check_jira_redhat.py \
  --cookie YOUR_JSESSIONID \
  --projects
```

### Search Issues
```bash
python3 check_jira_redhat.py \
  --cookie YOUR_JSESSIONID \
  --search "project = PROJ AND status = Open"
```

## Important Notes

⚠️ **Security Considerations:**
- JSESSIONID cookies expire when you log out or after a period of inactivity
- Don't share cookies or commit them to git
- Store them securely (use environment variables)
- Cookies are session-specific and tied to your login

⚠️ **Cookie Expiration:**
- Cookies typically expire after:
  - Logging out
  - Extended inactivity (varies by Red Hat policy)
  - Browser session ends (if session cookies)
  
If you get authentication errors, get a fresh cookie by logging in again.

## Alternative: Personal Access Token (If Available)

If Red Hat Jira supports Personal Access Tokens (check Jira settings):
1. Log into https://issues.redhat.com
2. Go to **Profile** → **Account Settings** → **Security**
3. Look for **API Tokens** or **Personal Access Tokens**
4. Create a new token
5. Use it with the standard `check_jira.py` script

However, based on testing, Red Hat Jira appears to require SSO, so cookie-based authentication is the most reliable method.

## Troubleshooting

### "403 Forbidden" or "401 Unauthorized"
- Cookie might have expired → Get a new one by logging in again
- Cookie might be invalid → Make sure you copied the entire value
- Session might have ended → Log in again and get fresh cookie

### "HTML Response Instead of JSON"
- This usually means SSO redirect → Use cookie-based auth instead
- The token you have might be for a different purpose

### Connection Works But No Data
- Check your Jira permissions
- Verify you have access to the projects/issues you're querying
- Some endpoints might require additional permissions

---

**Next Steps:**
1. Log into https://issues.redhat.com
2. Extract JSESSIONID cookie from browser
3. Test with: `python3 check_jira_redhat.py --cookie YOUR_COOKIE --test`




