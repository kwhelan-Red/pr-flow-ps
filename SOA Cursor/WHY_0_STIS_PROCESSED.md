# Why 0 STIs Were Processed - Troubleshooting

## Common Reasons

### 1. Browser Automation Not Installed

**Check:**
```bash
python3 -c "from playwright.async_api import async_playwright; print('Playwright OK')"
```

**If error, install:**
```bash
pip install --break-system-packages playwright
playwright install chromium
```

### 2. ServiceNow Authentication Required

The browser opens but you need to log in manually:
- Browser window will open
- Log into ServiceNow when prompted
- Extraction will continue after login

### 3. STI Not Found in ServiceNow

Some STIs may not exist in ServiceNow:
- Check if STI exists: Search in ServiceNow manually
- STI name might be different
- STI might be retired/deleted

### 4. Search Query Not Working

The search might not find STIs:
- ServiceNow search syntax might have changed
- STI might be in a different table
- Need to search by Application ID instead of name

## Test First

Before running all 114 STIs, test with a few:

```bash
python3 test_extraction.py --max 3
```

This will:
- Test on 3 STIs
- Show you what's happening
- Help identify issues

## Manual Steps to Verify

1. **Open ServiceNow manually:**
   - Go to: https://redhat.service-now.com/cmdb_ci_business_app_list.do
   - Search for "AAP-001"
   - See if it exists

2. **Check browser automation:**
   ```bash
   python3 -c "from playwright.async_api import async_playwright; print('OK')"
   ```

3. **Test extraction:**
   ```bash
   python3 test_extraction.py --max 1
   ```

## Alternative: Use Manual Extraction

If automated extraction isn't working:

1. **Use Dashboard:**
   - Start dashboard: `python3 dashboard_enhanced.py`
   - Open: http://localhost:5000
   - Process STIs manually one by one

2. **Use Command Line:**
   ```bash
   python3 process_console_output.py --sti AAP-001 --json '<JSON>'
   ```

## Next Steps

1. Install Playwright (if not installed)
2. Test with 3 STIs: `python3 test_extraction.py --max 3`
3. Check results
4. If successful, run full extraction




