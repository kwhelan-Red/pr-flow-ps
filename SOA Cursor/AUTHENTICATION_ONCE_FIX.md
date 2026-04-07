# Fixed: Authentication Only Once + Better Error Handling

## Issues Fixed

### 1. API Error: "Unexpected token '<'"
**Problem**: Browser was getting HTML instead of JSON  
**Fix**: Added proper error handling to check response status and content type before parsing JSON

### 2. Authentication Every STI
**Problem**: Still asking for authentication for each STI  
**Fix**: 
- Authentication check removed from individual STI extraction
- Only authenticates ONCE at the start
- Persistent browser context saves cookies automatically
- If redirected to login (rare), just logs a warning but doesn't wait

## How It Works Now

### Authentication Flow:
1. **Browser opens** → Creates persistent context (saves cookies)
2. **Authenticate ONCE** → Check if login needed, wait if so
3. **Cookies saved** → Persistent context automatically saves session
4. **All STIs processed** → Uses saved cookies, NO re-authentication

### What You'll See:

**First Run:**
```
🌐 Browser opened - ONE window will stay open for all STIs
   Using persistent session (NOT private mode) - cookies will be saved
   🔐 Authenticating ONCE - session will be reused for all STIs

🔐 Checking authentication status...
⚠️  Authentication required! (only if needed)
   Please complete SSO login in the browser window.
   This is the ONLY time you'll need to authenticate.

✅ Authentication verified! Cookies saved - will be reused for all STIs.

[1/114] Processing AAP-001...
🔍 Searching for AAP-001...
✅ AAP-001: Extracted successfully

[2/114] Processing ATLA-001...
🔍 Searching for ATLA-001...
✅ ATLA-001: Extracted successfully
```

**Subsequent Runs:**
```
🌐 Browser opened - ONE window will stay open for all STIs
   Using persistent session (NOT private mode) - cookies will be saved
   🔐 Authenticating ONCE - session will be reused for all STIs

🔐 Checking authentication status...
✅ Already authenticated! Using saved session.

[1/114] Processing AAP-001...
🔍 Searching for AAP-001...
✅ AAP-001: Extracted successfully
```

## Key Changes

1. **Removed authentication check from `extract_with_playwright()`** - No longer checks auth for each STI
2. **Single authentication at start** - Only checks once when browser opens
3. **Better error handling** - API errors now show more details
4. **Cookie verification** - Checks if cookies are saved after authentication

## If You Still See Login Prompts

If you still see login prompts for each STI, it might mean:
1. Cookies aren't persisting (check browser console)
2. ServiceNow session expired (complete login once more)
3. Browser cache issue (restart browser)

The persistent context should save cookies automatically. If it's not working, the user data directory might need to be cleared.

## Testing

To test:
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 test_extraction.py --max 3
```

You should only see authentication prompt ONCE at the start, then all 3 STIs process without asking for auth again.



