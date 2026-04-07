# Complete ESS, PIA, SIA Field Location Guide

**Date:** January 16, 2026  
**Based on:** ATROPOS (ATRO-001) analysis

---

## ✅ CONFIRMED FIELD LOCATIONS

### ESS (Enterprise Security Standards) Self-Assessment
- **Tab:** Compliance
- **Field Name:** "Security (ESS) assessment URL"
- **Field Type:** URL field (clickable link)
- **Location in Tab:** Visible after clicking Compliance tab, scroll to find
- **Status Determination:** 
  - URL present = Assessment exists (In Progress or Complete)
  - URL absent/empty = Not Started

### PIA (Privacy Impact Assessment)
- **Tab 1:** Compliance
  - **Field:** "Privacy (PIA) assessment URL"
  - **Type:** URL field (clickable link)
- **Tab 2:** Data Privacy
  - **Field:** "DPQ Complete"
  - **Type:** Checkbox or status field
  - **Location:** Scroll down in Data Privacy tab
- **Status Determination:**
  - PIA URL present + DPQ Complete = true = Complete
  - PIA URL present + DPQ Complete = false = In Progress
  - PIA URL absent = Not Started

### SIA (Service Impact Assessment)
- **Status:** Location not yet determined
- **Checked Locations:**
  - Support tab - Not found
  - Compliance tab - Not found
  - Data Privacy tab - Not found
- **Possible Locations:**
  - Related Lists section
  - Other tabs (Access Revalidation, CI Relationships)
  - Separate related records
  - May be named differently (e.g., "Service Impact", "Business Impact")

---

## 📋 COLLECTION WORKFLOW

For each of 283 CMDB IDs:

1. **Navigate to Business Application detail page**
   - Use URL: `https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id={sys_id}`
   - Or click from list view

2. **Extract Basic Info**
   - Application ID (CMDB ID)
   - Application Name

3. **Click "Compliance" Tab**
   - Find "Security (ESS) assessment URL" field
   - Extract URL value (if present)
   - Find "Privacy (PIA) assessment URL" field
   - Extract URL value (if present)

4. **Click "Data Privacy" Tab**
   - Scroll down to find "DPQ Complete" field
   - Extract checkbox/status value

5. **Search for SIA**
   - Check Support tab
   - Check other tabs
   - Check Related Lists
   - Search page for "Service Impact" or "SIA"

6. **Determine Status**
   - ESS: URL present = exists, URL absent = Not Started
   - PIA: URL + DPQ Complete = Complete, URL only = In Progress, No URL = Not Started
   - SIA: To be determined once location found

7. **Navigate to Next Record**
   - Use navigation arrows or URL pattern

---

## 🔍 FIELD EXTRACTION NOTES

**ESS Assessment URL:**
- Field is read-only
- May be empty or contain a URL
- URL format: Typically ServiceNow or external assessment tool URL

**PIA Assessment URL:**
- Field is read-only
- May be empty or contain a URL
- URL format: Typically ServiceNow or external assessment tool URL

**DPQ Complete:**
- Checkbox field in Data Privacy tab
- Values: true/false or checked/unchecked
- Indicates Privacy Data Questionnaire completion status

---

## 📊 STATUS MAPPING

| Field State | ESS Status | PIA Status |
|------------|-----------|------------|
| URL Present | Assessment Exists | Assessment Exists |
| URL Absent | Not Started | Not Started |
| DPQ Complete = true | N/A | Complete |
| DPQ Complete = false | N/A | In Progress (if URL present) |

---

## ⚠️ CHALLENGES

1. **Browser Navigation:** Direct URL navigation and arrow buttons don't reliably work
2. **Field Value Extraction:** URL fields may not show values in browser snapshots
3. **SIA Location:** Still needs to be determined
4. **Status Interpretation:** URLs indicate existence but not completion status (except DPQ Complete for PIA)

---

## 🚀 RECOMMENDED APPROACH

**FASTEST:** Export from ServiceNow list page
- Export all 283 records to CSV
- Process with `extract_ess_pia_sia_status.py`
- All fields will be included in export

**ALTERNATIVE:** Continue manual collection
- Use established pattern
- Navigate through all 283 records
- Extract ESS, PIA, SIA from each
- Time: 30-60 minutes

---

**Records Analyzed:** 1 of 283 (ATROPOS - ATRO-001)  
**Field Locations:** ✅ Confirmed  
**Collection Pattern:** ✅ Established  
**Ready to:** Continue collection or process export




