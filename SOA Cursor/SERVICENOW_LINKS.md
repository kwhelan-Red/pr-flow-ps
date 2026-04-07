# ServiceNow Links for SOA Data Extraction

## Main Links

### 1. Business Applications List (All SOA Applicable)
**Full URL:**
```
https://redhat.service-now.com/now/nav/ui/classic/params/target/cmdb_ci_business_app_list.do%3Fsysparm_query%3Dinstall_statusNOT%2520IN7%252C21%252C22%255Eu_soa_applicable%253Dtrue%26sysparm_first_row%3D1%26sysparm_view%3D
```

**Simplified (easier to read):**
```
https://redhat.service-now.com/cmdb_ci_business_app_list.do?sysparm_query=install_statusNOT%20IN7,21,22^u_soa_applicable=true
```

This shows all Business Applications that:
- Are not retired/retiring (install_status NOT IN 7,21,22)
- Are SOA applicable (u_soa_applicable=true)

### 2. Individual Business Application Page
**URL Pattern:**
```
https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=<SYS_ID>
```

**Example (ATROPOS):**
```
https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=0057625a1be086101fbd64e9bc4bcbc4
```

### 3. Business Applications Dashboard
```
https://redhat.service-now.com/$pa_dashboard.do?sysparm_dashboard=6e6c977747d49a50cf3edd9c716d4335&sysparm_tab=fb7c5b7747d49a50cf3edd9c716d43d9
```

## How to Find sys_id for Each STI

1. **Go to Business Applications List** (link #1 above)
2. **Search for your STI** in the search box (e.g., type "AAP-001")
3. **Click on the application** in the results
4. **Look at the URL** - you'll see something like:
   ```
   https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=0057625a1be086101fbd64e9bc4bcbc4
   ```
5. **Copy the sys_id** (the long string after `sys_id=`)
6. **Use it** in the individual application URL pattern

## Quick Access

- **Base URL:** https://redhat.service-now.com
- **Business Apps List:** https://redhat.service-now.com/cmdb_ci_business_app_list.do
- **Search by Application ID:** Use the search box on the list page

## For Extraction

Once you're on an individual Business Application page:

1. **Click the "Compliance" tab** (to see ESS and PIA URLs)
2. **Press F12** to open browser console
3. **Run the JavaScript extraction script** (from QUICK_START.md)
4. **Copy the JSON output**
5. **Process with:** `python3 process_console_output.py --sti <STI> --json '<JSON>'`

## Example Workflow

1. Open: https://redhat.service-now.com/cmdb_ci_business_app_list.do?sysparm_query=install_statusNOT%20IN7,21,22^u_soa_applicable=true
2. Search for "AAP-001"
3. Click on AAP-001
4. Note the sys_id from URL (e.g., `sys_id=abc123...`)
5. Use that sys_id to create direct link: `https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=abc123...`
6. Extract data using JavaScript console script




