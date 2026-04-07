# Red Hat Jira Setup Summary

## Current Status

**Jira URL:** `https://issues.redhat.com`  
**Username:** `rh-ee-kwhelan`  
**Token Provided:** `[redacted — store in environment / local config only]`  
**JSESSIONID Provided:** `[redacted — paste a fresh value from your browser when testing]`

## Authentication Challenge

Red Hat Jira uses **SAML/SSO authentication** which makes standard API token authentication difficult. The system redirects to Red Hat SSO for authentication.

## What We Need

### Option 1: Fresh JSESSIONID Cookie (Recommended)

1. **Log into Jira** (make sure you're actively logged in)
   - Go to https://issues.redhat.com
   - Complete SSO login if prompted

2. **Get Fresh Cookie**
   - Open Developer Tools (F12)
   - Application → Cookies → `https://issues.redhat.com`
   - Copy `JSESSIONID` value
   - **Important:** Get it while you're actively logged in and the page is loaded

3. **Test Connection**
   ```bash
   python3 check_jira_redhat.py --cookie YOUR_FRESH_JSESSIONID --test
   ```

### Option 2: Check for Personal Access Token in Jira

1. Log into https://issues.redhat.com
2. Go to **Profile** (your avatar) → **Account Settings**
3. Look for **Security** or **API Tokens** section
4. Check if there's an option to create a Personal Access Token
5. If available, create one and use it with `check_jira.py`

### Option 3: Use the Token with Different Method

The API token (kept out of git; set locally) might work with:
- A different authentication endpoint
- OAuth 2.0 flow
- A specific Red Hat API gateway

## Next Steps

**Please provide one of the following:**

1. **Fresh JSESSIONID** - Get it from browser while actively logged into Jira
2. **Confirmation** - If the token format is correct and where it should be used
3. **Documentation** - Any specific instructions from the BragAI setup document about Red Hat Jira authentication

## Files Available

- `check_jira.py` - Standard Jira API client (for Jira Cloud)
- `check_jira_redhat.py` - Cookie-based client for Red Hat Jira
- `check_jira_cookie.py` - Simple cookie test script

## Testing

Once you provide a fresh JSESSIONID, we can:
- ✅ Test connection
- ✅ List all projects
- ✅ Search issues
- ✅ Get project details
- ✅ Query boards and sprints

---

**Ready when you have a fresh JSESSIONID from an active browser session!**




