# CMDB IDs That Need SOA Assessments

**Source:** ServiceNow Business Applications  
**URL:** https://redhat.service-now.com/now/nav/ui/classic/params/target/cmdb_ci_business_app_list.do?sysparm_query=install_statusNOT%20IN7,21,22^u_soa_applicable=true

**Filter Applied:**
- Status: NOT IN (Retired, Archived, Cancelled/Invalid Record)
- SOA Applicable: true

**Total Records:** 283

---

## Current Status

From the ServiceNow page, I can see:
- **Total Records:** 283 applications
- **Records per page:** 20
- **Total pages:** ~15 pages

**Sample Application IDs visible:**
1. ATRO-001 - ATROPOS
2. RHBQ-003 - RHBQ Prod  
3. PRP-001 - rhel-prp (Alias: EXD/SP)

---

## How to Extract All 283 CMDB IDs

### Option 1: Export from ServiceNow (Recommended)

1. **On the ServiceNow page**, look for:
   - "Actions on selected rows..." dropdown menu
   - Or a gear/settings icon
   - Or right-click on the table

2. **Select "Export" or "Export to CSV"**
   - This will export all 283 records
   - Make sure to export all columns, especially "Application ID"

3. **Save the CSV file** to your Downloads folder

4. **Process the export:**
   ```bash
   python3 extract_soa_applicable_cmdb_ids.py "/path/to/export.csv" --output "SOA_Applicable_CMDB_IDs.xlsx"
   ```

### Option 2: Manual Collection (if export not available)

Since there are 283 records across ~15 pages, you would need to:
1. Navigate through each page
2. Copy the Application IDs from each page
3. Combine them into a list

This is time-consuming, so **Option 1 (Export) is strongly recommended**.

---

## Processing Script

I've created `extract_soa_applicable_cmdb_ids.py` which will:
- Read the ServiceNow CSV export
- Extract all Application IDs (CMDB IDs)
- Create an Excel file with:
  - Sheet 1: All CMDB IDs with application names
  - Sheet 2: Summary statistics

---

## Expected Output

Once processed, you'll have:
- **283 CMDB IDs** that need SOA assessments
- List sorted alphabetically
- Application names for reference
- Ready to match with SOAR project STIs

---

## Next Steps

1. ✅ Page accessed - 283 records identified
2. ⏳ Export data from ServiceNow
3. ⏳ Process export with script
4. ⏳ Create final list of CMDB IDs needing SOA assessments
5. ⏳ Match with SOAR STIs (if needed)

---

**Note:** The ServiceNow page is currently loaded and showing the filtered list. To get all 283 CMDB IDs, please export the table data.




