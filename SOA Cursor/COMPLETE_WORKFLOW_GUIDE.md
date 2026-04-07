# SOA Data Extraction - Complete Workflow Guide

## Overview

This guide covers three methods for extracting SOA data from ServiceNow:
1. **Manual Console Execution** (with automated CSV processing)
2. **Browser Automation** (Playwright/Selenium)
3. **Batch Processing** (for multiple extractions)

---

## Method 1: Manual Console Execution (Recommended for Start)

### Quick Start

1. **Navigate to ServiceNow page** for an STI (e.g., ATRO-001)
2. **Open browser console** (F12)
3. **Run extraction script** (copy from `execute_extraction.js`)
4. **Copy JSON output** from console
5. **Process output:**
   ```bash
   python3 process_console_output.py --sti ATRO-001 --json '{"applicationName":"ATROPOS",...}'
   ```

### Detailed Steps

#### Step 1: Prepare
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 create_workflow.py  # Creates workflow guide
```

#### Step 2: Extract Values
1. Go to ServiceNow: `https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=<SYS_ID>`
2. Open console (F12)
3. Click "Compliance" tab
4. Paste and run JavaScript from `execute_extraction.js`
5. Copy the JSON output

#### Step 3: Process Output

**Option A: Direct JSON string**
```bash
python3 process_console_output.py --sti ATRO-001 --json '{"applicationName":"ATROPOS","criticalityTier":"C1",...}'
```

**Option B: From file**
```bash
# Save JSON to file
echo '{"applicationName":"ATROPOS",...}' > console_outputs/ATRO-001.json

# Process file
python3 process_console_output.py --sti ATRO-001 --file console_outputs/ATRO-001.json
```

**Option C: Interactive (paste JSON)**
```bash
python3 process_console_output.py --sti ATRO-001
# Then paste JSON and press Ctrl+D
```

#### Step 4: Verify
```bash
python3 check_extraction_status.py
```

---

## Method 2: Browser Automation (Fully Automated)

### Setup

**Playwright (Recommended):**
```bash
pip install playwright
playwright install chromium
```

**Selenium:**
```bash
pip install selenium
# Install ChromeDriver separately
```

### Usage

**Single STI:**
```bash
python3 browser_automation_integration.py \
  --method playwright \
  --sti ATRO-001 \
  --url "https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=0057625a1be086101fbd64e9bc4bcbc4"
```

**Batch (requires sys_id mapping):**
```bash
# First, create STI -> sys_id mapping file
# Then modify script to use mapping
python3 browser_automation_integration.py --method playwright --all
```

---

## Method 3: Batch Processing

### Process Multiple Console Outputs

1. **Save JSON files** to a directory:
   ```bash
   mkdir console_outputs
   # Save each STI's JSON as: console_outputs/ATRO-001.json
   ```

2. **Process all at once:**
   ```bash
   python3 batch_process_console.py --input-dir console_outputs
   ```

---

## File Structure

```
SOA Cursor/
├── soa_data_all_stis.csv          # Main CSV file
├── soa_stis_list.json             # List of all STIs
├── execute_extraction.js           # JavaScript extraction script
├── process_console_output.py      # Process manual console output
├── batch_process_console.py       # Batch processor
├── browser_automation_integration.py  # Browser automation
├── check_extraction_status.py     # Check progress
└── create_workflow.py             # Generate workflow guide
```

---

## Workflow Comparison

| Method | Speed | Automation | Setup Complexity |
|--------|-------|------------|------------------|
| Manual Console | Medium | Low | Low |
| Browser Automation | Fast | High | Medium |
| Batch Processing | Fast | Medium | Low |

---

## Tips

1. **Start with Manual Method** to understand the process
2. **Use Batch Processing** when you have multiple JSON files
3. **Use Browser Automation** for full automation (requires sys_id mapping)
4. **Check Status Regularly** with `check_extraction_status.py`

---

## Troubleshooting

### JSON Parse Errors
- Ensure JSON is valid (use JSON validator)
- Check for extra characters or formatting issues
- Try saving to file first, then processing

### CSV Update Errors
- Verify STI exists in CSV: `grep "ATRO-001" soa_data_all_stis.csv`
- Check CSV file permissions
- Ensure CSV is not open in another program

### Browser Automation Errors
- Verify authentication to ServiceNow
- Check network connectivity
- Ensure sys_id is correct
- Wait for page to fully load

---

## Next Steps

1. ✅ Choose extraction method
2. ✅ Extract values for first STI
3. ✅ Verify CSV update
4. ✅ Continue with remaining STIs
5. ✅ Check final status




