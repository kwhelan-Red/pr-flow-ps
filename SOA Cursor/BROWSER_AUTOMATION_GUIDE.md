# Browser Automation Integration Guide

This guide explains how to use browser automation tools (Playwright or Selenium) to automatically extract SOA data from ServiceNow.

## Prerequisites

### Option 1: Playwright (Recommended)
```bash
pip install playwright
playwright install chromium
```

### Option 2: Selenium
```bash
pip install selenium
# Also need ChromeDriver: https://chromedriver.chromium.org/
```

## Usage

### Single STI Extraction

**Playwright:**
```bash
python3 browser_automation_integration.py \
  --method playwright \
  --sti ATRO-001 \
  --url "https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=0057625a1be086101fbd64e9bc4bcbc4"
```

**Selenium:**
```bash
python3 browser_automation_integration.py \
  --method selenium \
  --sti ATRO-001 \
  --url "https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=0057625a1be086101fbd64e9bc4bcbc4"
```

### Batch Extraction

To extract all STIs, you'll need to:
1. Create a mapping file (STI -> sys_id)
2. Modify the script to use the mapping
3. Run batch extraction

## How It Works

1. **Navigate** to ServiceNow Business Application page
2. **Wait** for page to load
3. **Click** Compliance tab (if needed)
4. **Execute** JavaScript extraction script
5. **Capture** return value (JSON object)
6. **Update** CSV with extracted values

## Advantages

- ✅ Fully automated
- ✅ No manual console interaction
- ✅ Can process all STIs in batch
- ✅ Reliable value extraction
- ✅ Supports JavaScript execution

## Limitations

- Requires sys_id for each STI (need to search ServiceNow first)
- May need authentication handling
- ServiceNow may have rate limiting




