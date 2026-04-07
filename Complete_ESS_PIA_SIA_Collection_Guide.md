# Complete Guide: Collect ESS, PIA, SIA Status for All 283 CMDB IDs

**Objective:** Extract Enterprise Security Standards (ESS) Self-Assessment, Privacy Impact Assessment (PIA), and Service Impact Assessment (SIA) status for all 283 CMDB IDs that need SOA assessments.

---

## Current Situation

- ✅ ServiceNow page loaded: https://redhat.service-now.com/now/nav/ui/classic/params/target/cmdb_ci_business_app_list.do?sysparm_query=install_statusNOT%20IN7,21,22^u_soa_applicable=true
- ✅ 283 total records identified
- ✅ Filter: SOA Applicable = true, Status not in (Retired, Archived, Cancelled)
- ⏳ ESS, PIA, SIA status collection needed

---

## Method 1: Export from ServiceNow (FASTEST - 2 minutes)

### Steps:

1. **On the ServiceNow page**, look for:
   - **"Actions on selected rows..."** dropdown (top right of table)
   - Or right-click on the table
   - Or look for a gear/settings icon

2. **Select "Export" or "Export to CSV"**
   - Make sure to export **ALL columns** (not just visible ones)
   - ServiceNow exports typically include ESS, PIA, SIA status fields

3. **Save the CSV file** to Downloads

4. **Process the export:**
   ```bash
   python3 extract_ess_pia_sia_status.py "/Users/kwhelan/Downloads/your_export.csv" --output "CMDB_ESS_PIA_SIA_Status.xlsx"
   ```

5. **Result:** Excel file with all 283 CMDB IDs and their ESS, PIA, SIA status

---

## Method 2: Browser Automation (SLOW - 30-60 minutes)

If export is not available, I can automate clicking through all 283 records:

1. Click first application (e.g., ATROPOS)
2. Wait for detail page to load
3. Extract ESS status
4. Extract PIA status
5. Extract SIA status
6. Extract Application ID
7. Navigate back to list
8. Repeat for all 283 records

**Note:** This is very slow and may encounter issues with ServiceNow's dynamic loading.

---

## Method 3: ServiceNow API (If Available)

If you have ServiceNow API access, I can create a script to query all records directly:

```python
# Query ServiceNow REST API
# Get all Business Applications with SOA Applicable = true
# Extract ESS, PIA, SIA status fields
```

---

## Expected Output

The final Excel file will contain:

### Sheet 1: ESS_PIA_SIA_Status
| CMDB ID | Application Name | ESS Self-Assessment Status | PIA Status | SIA Status |
|---------|------------------|---------------------------|------------|------------|
| ATRO-001 | ATROPOS | Complete | Complete | In Progress |
| RHBQ-003 | RHBQ Prod | Pending | Not Required | Complete |
| ... | ... | ... | ... | ... |
| (283 rows) | | | | |

### Sheet 2: Summary
- Total CMDB IDs: 283
- ESS Complete: X (Y%)
- ESS In Progress: X (Y%)
- PIA Complete: X (Y%)
- SIA Complete: X (Y%)

---

## Files Created

1. ✅ `extract_ess_pia_sia_status.py` - Process ServiceNow export
2. ✅ `ESS_PIA_SIA_Status_Instructions.md` - Detailed instructions
3. ✅ `CMDB_ESS_PIA_SIA_Status_Report.md` - Report template
4. ✅ `Complete_ESS_PIA_SIA_Collection_Guide.md` - This guide

---

## Next Action

**Please choose one:**

**A) Export the data from ServiceNow** (I'll process it immediately)  
**B) I'll start clicking through all 283 records** (will take time)  
**C) Provide ServiceNow API credentials** (I'll query directly)

---

**Current Status:** Ready to proceed once data is available or you confirm to start automated clicking.




