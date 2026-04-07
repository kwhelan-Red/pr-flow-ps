# CMDB IDs - ESS, PIA, SIA Status Report

**Source:** ServiceNow Business Applications  
**Filter:** SOA Applicable = true  
**Total Records:** 283 CMDB IDs

**Date:** January 15, 2026

---

## Required Information

For each of the **283 CMDB IDs**, we need to extract:

1. **Enterprise Security Standards (ESS) Self-Assessment** Status
2. **Privacy Impact Assessment (PIA)** Status
3. **Service Impact Assessment (SIA)** Status

---

## Current Status

✅ **ServiceNow page accessed**  
✅ **283 records identified**  
⏳ **Status collection in progress**

---

## Collection Method

### Recommended: Export from ServiceNow

The fastest way to get all ESS, PIA, SIA status is to:

1. **On the ServiceNow page:**
   - Click **"Actions on selected rows..."** dropdown
   - Select **"Export"** or **"Export to CSV"**
   - Make sure all columns are included (especially ESS, PIA, SIA fields)

2. **Process the export:**
   ```bash
   python3 extract_ess_pia_sia_status.py "/path/to/export.csv" --output "CMDB_ESS_PIA_SIA_Status.xlsx"
   ```

### Alternative: Manual Collection via Browser

If export is not available, I can click through each of the 283 applications:
- Click application name → View detail page → Extract ESS/PIA/SIA → Navigate back
- Estimated time: 30-60 minutes
- This will be automated but slow

---

## Expected Output Format

| CMDB ID | Application Name | ESS Self-Assessment Status | PIA Status | SIA Status |
|---------|------------------|---------------------------|------------|------------|
| ATRO-001 | ATROPOS | [Status] | [Status] | [Status] |
| RHBQ-003 | RHBQ Prod | [Status] | [Status] | [Status] |
| PRP-001 | rhel-prp | [Status] | [Status] | [Status] |
| ... | ... | ... | ... | ... |
| (283 total) | | | | |

---

## Status Values (Typical)

**ESS Self-Assessment:**
- Complete
- In Progress
- Pending
- Not Started
- Not Required

**PIA:**
- Complete
- Required
- Not Required
- In Progress
- Pending

**SIA:**
- Complete
- Required
- Not Required
- In Progress
- Pending

---

## Next Steps

1. ⏳ Export data from ServiceNow OR
2. ⏳ Begin automated clicking through 283 records
3. ⏳ Extract ESS, PIA, SIA status for each
4. ⏳ Generate Excel report with all data

---

**Note:** The ServiceNow page is currently loaded. To proceed with automated collection, I'll need to either:
- Export the data (fastest)
- Or begin clicking through all 283 records (will take time)




