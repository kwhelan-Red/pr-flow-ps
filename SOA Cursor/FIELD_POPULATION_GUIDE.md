# Field Population Guide

## Issue
CSV fields are not populated because browser snapshots show field **locations** but not **values**.

## Solution Options

### Option 1: ServiceNow Export (RECOMMENDED - Fastest)
1. Navigate to ServiceNow Business Applications
2. Filter: `SOA Applicable = true`
3. Click "Actions on selected rows..." → Export
4. Export to CSV (include all columns)
5. Run: `python3 get_soa_data.py --method export --export-file <export.csv>`
6. All fields automatically populated ✅

**Time: ~2 minutes**

### Option 2: Enhanced Browser Automation
Need to read actual DOM values:
- Read textbox `.value` properties
- Read combobox selected options
- Extract link href attributes
- Read all field values from page

**Time: ~30-60 minutes for 114 STIs**

### Option 3: Manual Collection
Navigate to each STI and copy values manually.

**Time: Several hours**

## Current Status
- CSV structure: ✅ Ready
- Field locations: ✅ Identified
- Field values: ❌ Need extraction

## Next Steps
1. Export from ServiceNow (recommended)
2. Or enhance browser automation to read DOM values
3. Populate CSV with extracted data

