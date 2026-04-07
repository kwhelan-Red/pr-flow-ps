# Getting SOA Approval Status from SOAR Project

## Current Situation

The JSESSIONID cookie works for basic Jira API calls (like `/rest/api/2/myself`), but returns **401 Unauthorized** when trying to access the SOAR project issues. This indicates:

1. **Permissions Issue**: Your account may not have API access to the SOAR project
2. **Cookie Scope**: The cookie might only work for certain endpoints
3. **Project Access**: You may need explicit project permissions

## Solutions

### Option 1: Manual Export from Jira UI (Recommended)

1. **Log into Jira** at https://issues.redhat.com
2. **Navigate to the SOAR project**:
   - Go to: https://issues.redhat.com/projects/SOAR/issues
   - Or use the filter: https://issues.redhat.com/projects/SOAR/issues/SOAR-3837?filter=allopenissues

3. **Export the data**:
   - In Jira, use the **Export** function (usually in the top right)
   - Export as **CSV** or **Excel**
   - The export should include all fields including SOA approval status

4. **Filter in Excel/CSV**:
   - Open the exported file
   - Look for columns related to "SOA", "Security Operating Approval", or "Approval"
   - Filter/sort by approval status

### Option 2: Use Jira JQL with Export

1. **Log into Jira**
2. **Go to Issues → Search for issues**
3. **Enter JQL query**:
   ```
   project = SOAR AND status != Closed AND status != Resolved
   ```
4. **Export results** as CSV/Excel
5. **Analyze the exported data** for SOA approval status

### Option 3: Request API Access

If you need programmatic access:
1. Contact your Jira administrator
2. Request API access permissions for the SOAR project
3. Or request a Personal Access Token with SOAR project access

### Option 4: Check if SOA Field Name is Different

The SOA field might be named differently in your Jira instance. Common variations:
- `Security Operating Approval`
- `SOA Status`
- `SOA Approval`
- `Operating Approval`
- Custom field ID (like `customfield_12345`)

To find the exact field name:
1. Open any SOAR issue in Jira
2. Look at all the fields displayed
3. Find the one related to SOA approval
4. Note the exact field name

## Script Ready

I've created `get_soar_soa_status.py` which will work once you have:
- A cookie with SOAR project access, OR
- API permissions for the SOAR project

## Next Steps

**If you can export the data manually:**
1. Export the SOAR issues as CSV/Excel
2. Share the file or the SOA approval data
3. I can help analyze it or create a script to process it

**If you want to use the API:**
1. Get a fresh JSESSIONID cookie while logged into Jira
2. Ensure you have access to the SOAR project
3. Run: `python3 get_soar_soa_status.py --cookie YOUR_COOKIE`

**If you can share the SOA field name:**
- I can update the script to look for the specific field name
- This will make the categorization more accurate

---

**Current Status:**
- ✅ Jira connection works (basic API)
- ❌ SOAR project access returns 401 (permissions issue)
- ✅ Script created and ready (`get_soar_soa_status.py`)
- ⏳ Waiting for: Either manual export data OR cookie with SOAR access




