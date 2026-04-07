# Access Revalidation Policy - Applications Under chrisw

**Date:** January 15, 2026  
**Policy Applicability:** Annual Access Revalidation Requirement

---

## Policy Statement

An annual (each calendar year) revalidation of administrative/privileged users is a requirement for applications with a **Criticality Rating of "C1"** or **Data Classification of "RH-RESTRICTED(+PII)"** thus encompassing C2-C4 systems that are not already performing more frequent access revalidation reviews that are required for SOX(FINSIG), ASCA or by the RH Global Privacy team (see CMDB record, Access Revalidation tab for these assignments).

This review is to be executed by application owners identified in Red Hat's CMDB, available here: https://red.ht/business-app-listing, or individuals the owners have delegated this activity to.

To find a listing of applications you may be identified as an owner of, select **"Owned by"** in the search dropdown of the CMDB, and in the search field, enter your last name.

Red Hat has adopted this review in response to recommendations identified in both Internal Audit findings as well as comparisons between IBM and Red Hat security standards.

---

## Applications Under chrisw

**Manager:** chrisw  
**Search Method:** ServiceNow CMDB - Search by "Owned by" = chrisw

### How to Find Applications:

1. Navigate to: https://red.ht/business-app-listing
2. In the search dropdown, select **"Owned by"**
3. Enter: **chrisw** (or last name if different)
4. Review the list of applications

### Applications Requiring Annual Access Revalidation:

Applications that meet **ANY** of the following criteria require annual access revalidation:

- ✅ **Criticality Rating = "C1"**
- ✅ **Data Classification = "RH-RESTRICTED(+PII)"**
- ✅ **C2-C4 systems** (unless already performing more frequent reviews for SOX/FINSIG, ASCA, or RH Global Privacy)

**Exception:** Systems already performing more frequent access revalidation reviews (SOX/FINSIG, ASCA, RH Global Privacy) are exempt from this annual requirement.

---

## Application List Template

Once you have the list of applications under chrisw, use this template:

| Application Name | Application ID (CMDB) | Criticality Rating | Data Classification | Requires Annual Revalidation? | Current Revalidation Frequency | Notes |
|------------------|----------------------|-------------------|-------------------|------------------------------|------------------------------|-------|
| [App Name] | [APP-001] | [C1/C2/C3/C4] | [RH-RESTRICTED(+PII)/Other] | [Yes/No] | [Annually/Quarterly/Other] | [Any exceptions] |
| | | | | | | |

---

## Action Items

1. **Identify Applications:**
   - Search ServiceNow CMDB for applications owned by chrisw
   - Export the list to Excel/CSV for analysis

2. **Review Each Application:**
   - Check Criticality Rating (C1 requires revalidation)
   - Check Data Classification (RH-RESTRICTED(+PII) requires revalidation)
   - Check if already performing more frequent reviews (SOX/FINSIG, ASCA, Privacy)
   - Review Access Revalidation tab in CMDB record

3. **Apply Policy:**
   - For applications meeting criteria, ensure annual revalidation is scheduled
   - Document in CMDB Access Revalidation tab
   - Set next review date (annually, each calendar year)

4. **Documentation:**
   - Update CMDB records with revalidation schedule
   - Document any exceptions or delegations

---

## ServiceNow CMDB Access

**URL:** https://red.ht/business-app-listing  
**Alternative:** https://redhat.service-now.com/cmdb_ci_business_app_list.do

**Search Instructions:**
- Use "Owned by" filter
- Enter manager username or last name
- Export results for analysis

---

## Next Steps

1. ✅ Policy documented
2. ⏳ Extract applications under chrisw from ServiceNow
3. ⏳ Review each application against criteria
4. ⏳ Apply annual revalidation requirement where applicable
5. ⏳ Update CMDB records

---

**Note:** This document serves as a template. Once the actual list of applications under chrisw is extracted from ServiceNow, it should be populated in the table above.




