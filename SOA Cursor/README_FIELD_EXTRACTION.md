# Field Extraction Issue

## Problem
CSV fields are not populated because browser snapshots show field **locations** (refs, labels) but not field **values** (textbox.value, combobox.selectedValue).

## Root Cause
Browser automation snapshots capture:
- ✅ Element structure (refs, labels, roles)
- ❌ Element values (input values, selected options)

## Solutions

### Option 1: Browser Console Script (Manual)
1. Open ServiceNow page
2. Open browser console (F12)
3. Run `extract_values_console.js`
4. Copy extracted values
5. Update CSV manually

### Option 2: ServiceNow API (Automated)
Requires API authentication:
```
GET /api/now/table/cmdb_ci_business_app/{sys_id}
Fields: u_ess_url, u_pia_url, u_dpq_complete
```

### Option 3: Export Method (Fastest)
1. Export from ServiceNow UI
2. Run: `python3 get_soa_data.py --method export --export-file <file.csv>`
3. All fields automatically populated

## Current Status
- CSV structure: ✅ Ready
- Field locations: ✅ Identified
- Field values: ❌ Need extraction

