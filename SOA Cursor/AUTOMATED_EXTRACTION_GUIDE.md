# Automated Extraction Guide

## Overview

The automated extraction system can extract SOA data for all 114 STIs automatically from ServiceNow.

## Setup

### 1. Install Playwright (Recommended)

```bash
pip install playwright
playwright install chromium
```

Or install with system packages:
```bash
pip install --break-system-packages playwright
playwright install chromium
```

### 2. Start Enhanced Dashboard

```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 dashboard_enhanced.py
```

Or use the regular dashboard (it will use enhanced if available):
```bash
python3 dashboard.py
```

### 3. Open Browser

Navigate to: **http://localhost:5000**

## Using Automated Extraction

### Via Dashboard (Recommended)

1. **Start the dashboard** (see above)
2. **Open browser**: http://localhost:5000
3. **Click "Start Automated Extraction"** button
4. **Select options**:
   - Method: Playwright (recommended) or Selenium
   - Start From: STI index to start from (0 = beginning)
   - Max STIs: Maximum to process (leave empty for all)
5. **Monitor progress**:
   - Real-time status updates
   - Current STI being processed
   - Success/failure counts
   - Elapsed time

### Via Command Line

```bash
# Extract all STIs
python3 extract_all_automated.py --method playwright

# Extract first 10 STIs
python3 extract_all_automated.py --method playwright --max 10

# Start from STI index 50
python3 extract_all_automated.py --method playwright --start-from 50

# Install Playwright browsers
python3 extract_all_automated.py --install-playwright
```

## How It Works

1. **Search ServiceNow** for each STI
2. **Navigate** to the Business Application page
3. **Click Compliance tab** (for ESS/PIA URLs)
4. **Execute JavaScript** to extract field values
5. **Update CSV** automatically
6. **Show progress** on dashboard

## Requirements

- **ServiceNow Access**: You must be logged into ServiceNow
- **Browser**: Playwright/Selenium will open a browser window
- **Authentication**: You may need to authenticate when browser opens

## Troubleshooting

**"Playwright not installed"**
```bash
pip install playwright
playwright install chromium
```

**"Selenium not installed"**
```bash
pip install selenium
# Also need ChromeDriver
```

**"STI not found"**
- STI may not exist in ServiceNow
- Check STI name spelling
- Try manual extraction for that STI

**"Browser won't open"**
- Check if browser is already open
- Try closing other browser instances
- Check firewall settings

**"Authentication required"**
- Browser will open - log into ServiceNow manually
- Session may persist for subsequent extractions

## Progress Tracking

- **Real-time updates** on dashboard
- **Progress file**: `extraction_progress.json`
- **CSV updates**: `soa_data_all_stis.csv`

## Stopping Extraction

- **Via Dashboard**: Click "Stop Extraction" button
- **Via Command Line**: Press Ctrl+C
- **Kill process**: `pkill -f extract_all_automated.py`

## Best Practices

1. **Start small**: Test with `--max 5` first
2. **Monitor progress**: Watch dashboard for errors
3. **Resume**: Use `--start-from` to resume from where you left off
4. **Backup**: Export CSV before starting large extractions
5. **Rate limiting**: System includes delays between requests

## Current Status

Check extraction status:
```bash
python3 check_extraction_status.py
```

Or view on dashboard: http://localhost:5000




