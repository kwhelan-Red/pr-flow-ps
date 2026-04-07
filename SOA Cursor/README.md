# SOA Data Collection from ServiceNow

## Overview

This project contains scripts to collect Security Operating Approval (SOA) data from ServiceNow for all STIs.

## STIs Collected

- **Total STIs:** 114 unique STIs
- **Sources:**
  - Secure Flow Gaps: 58 STIs
  - SOAR Project: 61 STIs

## Collection Methods

### Method 1: Export Processing (RECOMMENDED - Fastest)

1. **Export from ServiceNow:**
   - Navigate to: Business Applications list
   - Filter: `SOA Applicable = true`
   - Click "Actions on selected rows..." → Export
   - Export to CSV (all fields)

2. **Process the export:**
   ```bash
   python3 get_soa_data.py --method export --export-file /path/to/servicenow_export.csv
   ```

3. **Output:**
   - `soa_data_all_stis.json` - Full data in JSON format
   - `soa_data_all_stis.xlsx` - Excel file with 2 sheets:
     - Sheet 1: SOA Data (all records)
     - Sheet 2: STI Summary (summary by STI)

### Method 2: Browser Automation

⚠️ Requires SSO authentication and may be slow

```bash
python3 get_soa_data.py --method browser
```

### Method 3: ServiceNow API

⚠️ Requires API credentials

```bash
python3 get_soa_data.py --method api
```

## Data Fields Collected

For each STI, the following data is collected:

- STI/CMDB ID
- Application Name
- SOA Status
- SOA Applicable
- ESS Self-Assessment Status
- ESS Assessment URL
- PIA Status
- PIA Assessment URL
- DPQ Complete
- SIA Status
- Criticality Tier
- Data Classification
- Install Status
- Last Updated

## Files

- `collect_soa_data.py` - Collect STI list from various sources
- `get_soa_data.py` - Main script to collect SOA data from ServiceNow
- `collect_soa_from_servicenow.py` - Browser automation template
- `soa_stis_list.json` - List of all STIs to process

## Next Steps

1. Export Business Applications from ServiceNow (SOA Applicable = true)
2. Run: `python3 get_soa_data.py --method export --export-file <export.csv>`
3. Review results in Excel file
