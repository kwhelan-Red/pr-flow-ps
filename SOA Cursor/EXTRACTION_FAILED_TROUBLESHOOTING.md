# Extraction Failed - Troubleshooting Guide

## What Happened

Your extraction completed but **1 STI failed**:
- **Processed**: 1 STI (AAP-001)
- **Failed**: 1 STI (AAP-001)

Looking at the results, AAP-001 was processed but got mostly "empty value" results:
- Application Name: "Business Applications" (this is the page title, not the actual app name)
- Criticality Tier: empty value
- ESS URL: empty value
- PIA URL: empty value
- DPQ Complete: empty value

## Why It Failed

The extraction likely failed because:

1. **STI Not Found**: The search didn't find AAP-001 in ServiceNow
2. **Wrong Page**: It found a generic "Business Applications" list page instead of the specific STI detail page
3. **Authentication Issue**: Not fully authenticated, so couldn't access the detail page
4. **Page Structure Changed**: ServiceNow page structure might be different than expected

## How to Fix

### Option 1: Test Extraction Manually (Recommended)

Test with a single STI to see what's happening:

```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 test_extraction.py --max 1
```

This will:
- Open browser
- Show you exactly what's happening
- Let you see if authentication is needed
- Show if STI is found

### Option 2: Check Authentication

The browser might need authentication:

1. **Run test extraction**:
   ```bash
   python3 test_extraction.py --max 1
   ```

2. **Watch the browser window**:
   - If it asks for SSO login, complete it
   - The script will wait for you (up to 5 minutes)

3. **Check if STI is found**:
   - Look for messages like "✅ Found and clicked STI link"
   - If you see "⚠️ STI not found", the STI might not exist in ServiceNow

### Option 3: Verify STI Exists

Check if AAP-001 exists in ServiceNow:

1. **Open ServiceNow manually**:
   - Go to: https://redhat.service-now.com/cmdb_ci_business_app_list.do
   - Search for "AAP-001"
   - See if it exists

2. **If it doesn't exist**:
   - The STI might be retired/deleted
   - Or the name might be different
   - Try searching by Application ID instead

### Option 4: Use Manual Extraction

If automated extraction isn't working, use manual extraction:

1. **Open Dashboard**:
   ```bash
   python3 launch_dashboard.py
   ```
   Then open: http://localhost:5000

2. **Process STI manually**:
   - Navigate to ServiceNow
   - Get JSON from browser console
   - Paste into dashboard

## Common Issues

### Issue: "STI not found in search results"
**Solution**: The STI might not exist or name is different. Check ServiceNow manually.

### Issue: "Could not find STI link"
**Solution**: ServiceNow search syntax might have changed. Try searching manually first.

### Issue: "Authentication required"
**Solution**: Complete SSO login in the browser window. The script will wait for you.

### Issue: "Business Applications" instead of actual app name
**Solution**: The script found the list page instead of detail page. STI link wasn't clicked properly.

## Next Steps

1. **Test with 1 STI first**:
   ```bash
   python3 test_extraction.py --max 1
   ```

2. **Watch the browser**:
   - See if authentication is needed
   - See if STI is found
   - See what errors appear

3. **Check the output**:
   - Look for "✅" messages (success)
   - Look for "⚠️" messages (warnings)
   - Look for "❌" messages (errors)

4. **If successful, run more**:
   ```bash
   python3 extract_all_automated.py --method playwright --max 5
   ```

## Current Status

- **Total STIs**: 114
- **Extracted**: 9 (7.9%)
- **Pending**: 105 (92.1%)

The failed extraction (AAP-001) didn't update the CSV because it got empty values. You can retry it after fixing the issue.



