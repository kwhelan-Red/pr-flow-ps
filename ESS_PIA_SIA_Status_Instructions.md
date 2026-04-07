# Extract ESS, PIA, SIA Status for All CMDB IDs

**Total Records:** 283 CMDB IDs that need SOA assessments  
**Source:** ServiceNow Business Applications (SOA Applicable = true)

---

## Required Information

For each of the 283 CMDB IDs, we need to extract:
1. **Enterprise Security Standards (ESS) Self-Assessment** status
2. **Privacy Impact Assessment (PIA)** status  
3. **Service Impact Assessment (SIA)** status

---

## Method 1: Export from ServiceNow (Recommended)

### Step 1: Export the Data

1. On the ServiceNow page showing 283 records:
   - Look for **"Actions on selected rows..."** dropdown
   - Or right-click on the table
   - Select **"Export"** or **"Export to CSV"**

2. **Important:** Make sure the export includes these columns:
   - Application ID (or CMDB ID)
   - Application Name
   - ESS Self-Assessment Status (or similar)
   - PIA Status (or similar)
   - SIA Status (or similar)

3. Save the CSV file

### Step 2: Process the Export

```bash
python3 extract_ess_pia_sia_status.py "/path/to/export.csv" --output "CMDB_ESS_PIA_SIA_Status.xlsx"
```

The script will:
- Auto-detect ESS, PIA, SIA status columns
- Extract status for all 283 CMDB IDs
- Create an Excel file with:
  - Sheet 1: All CMDB IDs with ESS, PIA, SIA status
  - Sheet 2: Summary statistics

---

## Method 2: Manual Collection (If Export Not Available)

If export is not available, you would need to:
1. Click on each of the 283 applications
2. View the detail page
3. Find ESS, PIA, SIA status fields
4. Record the status for each

**Note:** This is very time-consuming (283 clicks + data entry).

---

## Expected ServiceNow Column Names

The script will auto-detect columns, but common names include:

**ESS Status:**
- `ESS Status`
- `ESS Self-Assessment Status`
- `Enterprise Security Standards Status`
- `u_ess_status`
- `ESS Assessment Complete`

**PIA Status:**
- `PIA Status`
- `Privacy Impact Assessment Status`
- `u_pia_status`
- `PIA Complete`

**SIA Status:**
- `SIA Status`
- `Service Impact Assessment Status`
- `u_sia_status`
- `SIA Complete`

---

## Output Format

The Excel file will contain:

| CMDB ID | Application Name | ESS Self-Assessment Status | PIA Status | SIA Status |
|---------|------------------|---------------------------|------------|------------|
| ATRO-001 | ATROPOS | Complete | Complete | In Progress |
| RHBQ-003 | RHBQ Prod | Pending | Not Required | Complete |
| ... | ... | ... | ... | ... |

Plus a summary sheet with statistics.

---

## Next Steps

1. ✅ Script created: `extract_ess_pia_sia_status.py`
2. ⏳ Export data from ServiceNow (283 records)
3. ⏳ Run script to extract ESS, PIA, SIA status
4. ⏳ Review results in Excel file

---

**Note:** If the ServiceNow export doesn't include ESS, PIA, SIA columns, you may need to:
- Export from individual application detail pages
- Or use ServiceNow API to query these fields
- Or manually collect the data




