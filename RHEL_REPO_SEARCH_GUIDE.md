# RHEL Repository Search in ServiceNow

This guide explains how to use the script to search ServiceNow for RHEL Repository links.

## Quick Start

### Basic Usage

```bash
python3 search_rhel_repo_servicenow.py
```

This will:
- Open a browser window
- Authenticate with ServiceNow (if needed)
- Search for RHEL repository-related records
- Save results to JSON and CSV files

### Custom Search Terms

```bash
# Search for specific terms
python3 search_rhel_repo_servicenow.py --terms RHEL repository

# Multiple terms
python3 search_rhel_repo_servicenow.py --terms RHEL repo repository
```

### Output Options

```bash
# Save only JSON
python3 search_rhel_repo_servicenow.py --output json

# Save only CSV
python3 search_rhel_repo_servicenow.py --output csv

# Save both (default)
python3 search_rhel_repo_servicenow.py --output both
```

## Prerequisites

### Install Playwright

```bash
pip install --break-system-packages playwright
playwright install chromium
```

## How It Works

1. **Opens Browser**: Uses Playwright with persistent session (saves cookies)
2. **Authenticates**: If not already logged in, you'll need to complete SSO login once
3. **Searches Multiple Methods**:
   - Business Applications list with search query
   - CMDB list search
   - Global ServiceNow search
4. **Extracts Results**: Finds all matching records with links and details
5. **Saves Results**: Exports to JSON and/or CSV files

## Output Files

Results are saved with timestamps:
- `rhel_repo_search_results_YYYYMMDD_HHMMSS.json`
- `rhel_repo_search_results_YYYYMMDD_HHMMSS.csv`

### JSON Format

```json
{
  "searchDate": "2026-01-27T...",
  "totalResults": 5,
  "results": [
    {
      "name": "RHEL Repository",
      "link": "https://redhat.service-now.com/...",
      "detailLink": "https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=...",
      "allFields": ["Field1", "Field2", ...],
      "searchMethod": "Method 1"
    }
  ]
}
```

### CSV Format

All fields from results are exported as columns, making it easy to:
- Open in Excel
- Filter and sort
- Share with team

## Search Methods

The script tries multiple search approaches:

1. **Business Applications Search**: Searches in `cmdb_ci_business_app_list.do`
2. **CMDB List Search**: Searches in general CMDB items
3. **Global Search**: Uses ServiceNow's global search functionality

## Troubleshooting

### No Results Found

1. **Check Authentication**: Make sure you're logged into ServiceNow
2. **Try Different Terms**: The records might use different terminology
3. **Manual Search**: Try searching manually in ServiceNow first to verify records exist

### Browser Issues

- The browser window will stay open during the search
- If authentication is required, complete it in the browser window
- The session is saved, so you won't need to authenticate again

### Playwright Not Found

```bash
pip install --break-system-packages playwright
playwright install chromium
```

## Examples

### Search for RHEL Repositories

```bash
python3 search_rhel_repo_servicenow.py --terms RHEL repo
```

### Search for Red Hat Enterprise Linux Repos

```bash
python3 search_rhel_repo_servicenow.py --terms "Red Hat" "Enterprise Linux" repository
```

### Quick JSON Export

```bash
python3 search_rhel_repo_servicenow.py --output json
```

## Next Steps

After getting results:

1. **Review Results**: Check the JSON or CSV files
2. **Follow Links**: Use the `detailLink` to view full record details
3. **Extract Specific Data**: Use the links to navigate to individual records
4. **Export More Data**: If needed, use browser automation to extract additional fields

## Related Scripts

- `test_extraction.py` - Extract data from individual ServiceNow records
- `collect_from_servicenow.py` - Collect data for multiple STIs
- `extract_all_automated.py` - Automated extraction for all STIs
