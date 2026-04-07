#!/usr/bin/env python3
"""
Search ServiceNow for RHEL Repository links
Uses browser automation to search and extract RHEL repo information
"""

import asyncio
import json
import csv
from datetime import datetime
import sys
import os
import tempfile

# Check dependencies
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed")
    print("   Install: pip install --break-system-packages playwright")
    print("   Then: playwright install chromium")
    sys.exit(1)

# ServiceNow base URL
SERVICENOW_BASE = "https://redhat.service-now.com"

# JavaScript extraction script for search results
EXTRACTION_SCRIPT = """
(function() {
    var results = [];
    
    // Find all table rows in the results
    var rows = document.querySelectorAll('table.list2_body tbody tr, table.data_list_table tbody tr, .list_row');
    
    rows.forEach(function(row, index) {
        var record = {};
        
        // Get all cells in the row
        var cells = row.querySelectorAll('td, th');
        
        // Try to extract common fields
        var links = row.querySelectorAll('a');
        links.forEach(function(link) {
            var text = (link.textContent || link.innerText || '').trim();
            var href = link.href || '';
            
            // Application/Name link (usually first link)
            if (!record.name && text && text.length > 0 && !text.match(/^\\d+$/)) {
                record.name = text;
                record.link = href;
            }
            
            // Check if it's a detail page link
            if (href.includes('cmdb_ci') || href.includes('sys_id')) {
                record.detailLink = href;
            }
        });
        
        // Extract text from cells
        var cellTexts = [];
        cells.forEach(function(cell) {
            var text = (cell.textContent || cell.innerText || '').trim();
            if (text && text.length > 0) {
                cellTexts.push(text);
            }
        });
        
        if (cellTexts.length > 0) {
            record.allFields = cellTexts;
        }
        
        // Only add if we found something
        if (record.name || record.detailLink || (record.allFields && record.allFields.length > 0)) {
            record.rowIndex = index;
            results.push(record);
        }
    });
    
    return results;
})();
"""

async def wait_for_authentication(page, timeout=300):
    """Wait for user to complete SSO authentication if needed"""
    current_url = page.url
    
    # If already on ServiceNow main page (not login), skip check
    if 'redhat.service-now.com' in current_url and 'login' not in current_url.lower() and 'sso' not in current_url.lower() and 'auth' not in current_url.lower():
        try:
            has_servicenow_ui = await page.evaluate("""
                () => {
                    return document.querySelector('.navbar, .navpage, [id*="header"], .header') !== null ||
                           document.querySelector('body').innerText.includes('ServiceNow') ||
                           window.location.href.includes('redhat.service-now.com');
                }
            """)
            if has_servicenow_ui:
                return True
        except:
            pass
    
    # Only check if we're actually on a login/SSO page
    if 'login' in current_url.lower() or 'sso' in current_url.lower() or 'auth' in current_url.lower():
        print("⚠️  Authentication required!")
        print("   Please complete SSO login in the browser window.")
        print("   Waiting for authentication to complete (max 5 minutes)...")
        
        try:
            await page.wait_for_function(
                "() => !window.location.href.toLowerCase().includes('login') && !window.location.href.toLowerCase().includes('sso') && !window.location.href.toLowerCase().includes('auth')",
                timeout=timeout * 1000
            )
            print("✅ Authentication detected!")
            await page.wait_for_timeout(3000)
        except Exception as e:
            print(f"⚠️  Authentication timeout or error: {e}")
            print("   Continuing anyway - authentication may have completed")
            await page.wait_for_timeout(3000)
    
    return True

async def search_servicenow_rhel_repo(search_terms=None, base_url=SERVICENOW_BASE):
    """
    Search ServiceNow for RHEL Repository links
    
    Args:
        search_terms: List of search terms (default: ['RHEL', 'repo', 'repository'])
        base_url: ServiceNow base URL
    """
    if search_terms is None:
        search_terms = ['RHEL', 'repo']
    
    print("="*80)
    print("SEARCHING SERVICENOW FOR RHEL REPO LINKS")
    print("="*80)
    print(f"\n🔍 Search terms: {', '.join(search_terms)}")
    print(f"🌐 ServiceNow URL: {base_url}")
    print()
    
    results = []
    
    async with async_playwright() as p:
        # Use persistent user data directory to save cookies/sessions
        user_data_dir = os.path.join(tempfile.gettempdir(), 'playwright_servicenow_session')
        os.makedirs(user_data_dir, exist_ok=True)
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        print("🌐 Browser opened - using persistent session (cookies will be saved)")
        print()
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        # Authenticate if needed
        try:
            print("🔐 Checking authentication status...")
            await page.goto(f"{base_url}/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=60000)
            
            current_url = page.url
            if 'login' in current_url.lower() or 'sso' in current_url.lower() or 'auth' in current_url.lower():
                print("⚠️  Authentication required!")
                print("   Please complete SSO login in the browser window.")
                print("   This is the ONLY time you'll need to authenticate.\n")
                await wait_for_authentication(page)
                print("✅ Authentication complete! Session saved.\n")
            else:
                print("✅ Already authenticated! Using saved session.\n")
        except Exception as e:
            print(f"⚠️  Initial authentication check: {e}")
            print("   Continuing anyway - cookies may already be saved\n")
        
        # Try multiple search approaches
        search_queries = [
            # Search in Business Applications
            f"{base_url}/cmdb_ci_business_app_list.do?sysparm_query=nameLIKE{'%20OR%20nameLIKE'.join(search_terms)}",
            # Search with RHEL and repo
            f"{base_url}/cmdb_ci_business_app_list.do?sysparm_query=nameLIKE{'%20AND%20nameLIKE'.join(search_terms)}",
            # Search in all CMDB items
            f"{base_url}/cmdb_list.do?sysparm_query=nameLIKE{'%20OR%20nameLIKE'.join(search_terms)}",
        ]
        
        for i, search_url in enumerate(search_queries, 1):
            print(f"\n🔍 Search attempt {i}/{len(search_queries)}...")
            print(f"   URL: {search_url[:100]}...")
            
            try:
                await page.goto(search_url, wait_until='networkidle', timeout=60000)
                await page.wait_for_timeout(3000)  # Wait for page to load
                
                # Extract results
                print("   Extracting results...")
                page_results = await page.evaluate(EXTRACTION_SCRIPT)
                
                if page_results and len(page_results) > 0:
                    print(f"   ✅ Found {len(page_results)} results")
                    for result in page_results:
                        result['searchUrl'] = search_url
                        result['searchMethod'] = f"Method {i}"
                        results.append(result)
                else:
                    print("   ⚠️  No results found on this page")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
        
        # Also try using the search box if available
        print(f"\n🔍 Trying ServiceNow global search...")
        try:
            await page.goto(f"{base_url}/now/nav/ui/classic/params/target/search.do", wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(2000)
            
            # Look for search input
            search_input = await page.query_selector('input[name="sysparm_search"], input[id*="search"], input[type="search"]')
            if search_input:
                search_query = ' '.join(search_terms)
                print(f"   Entering search: {search_query}")
                await search_input.fill(search_query)
                await page.wait_for_timeout(1000)
                
                # Try to submit (look for submit button or press Enter)
                submit_button = await page.query_selector('button[type="submit"], input[type="submit"], button:has-text("Search")')
                if submit_button:
                    await submit_button.click()
                else:
                    await search_input.press('Enter')
                
                await page.wait_for_load_state('networkidle', timeout=30000)
                await page.wait_for_timeout(3000)
                
                # Extract results
                page_results = await page.evaluate(EXTRACTION_SCRIPT)
                if page_results and len(page_results) > 0:
                    print(f"   ✅ Found {len(page_results)} results from global search")
                    for result in page_results:
                        result['searchUrl'] = page.url
                        result['searchMethod'] = 'Global Search'
                        results.append(result)
        except Exception as e:
            print(f"   ⚠️  Global search not available or error: {e}")
        
        await context.close()
        print("\n🌐 Browser closed")
    
    return results

def save_results(results, output_format='json'):
    """Save search results to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if output_format == 'json':
        output_file = f"rhel_repo_search_results_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump({
                'searchDate': datetime.now().isoformat(),
                'totalResults': len(results),
                'results': results
            }, f, indent=2)
        print(f"\n✅ Results saved to: {output_file}")
        return output_file
    
    elif output_format == 'csv':
        output_file = f"rhel_repo_search_results_{timestamp}.csv"
        if results:
            # Get all unique field names
            fieldnames = set()
            for result in results:
                fieldnames.update(result.keys())
            fieldnames = sorted(list(fieldnames))
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for result in results:
                    # Flatten allFields array if present
                    row = result.copy()
                    if 'allFields' in row and isinstance(row['allFields'], list):
                        row['allFields'] = ' | '.join(row['allFields'])
                    writer.writerow(row)
            print(f"\n✅ Results saved to: {output_file}")
            return output_file
        else:
            print("\n⚠️  No results to save")
            return None
    
    return None

def print_results_summary(results):
    """Print a summary of search results"""
    print("\n" + "="*80)
    print("SEARCH RESULTS SUMMARY")
    print("="*80)
    print(f"\n📊 Total results found: {len(results)}")
    
    if not results:
        print("\n⚠️  No results found. Try:")
        print("   1. Check if you're logged into ServiceNow")
        print("   2. Try different search terms")
        print("   3. Search manually in ServiceNow to verify records exist")
        return
    
    print("\n📋 Results:")
    print("-"*80)
    
    for i, result in enumerate(results[:20], 1):  # Show first 20
        print(f"\n{i}. {result.get('name', 'Unknown')}")
        if result.get('link'):
            print(f"   Link: {result['link']}")
        if result.get('detailLink'):
            print(f"   Detail: {result['detailLink']}")
        if result.get('allFields'):
            fields = result['allFields']
            if isinstance(fields, list):
                print(f"   Fields: {', '.join(fields[:5])}...")  # Show first 5 fields
            else:
                print(f"   Fields: {fields[:100]}...")
        print(f"   Method: {result.get('searchMethod', 'Unknown')}")
    
    if len(results) > 20:
        print(f"\n... and {len(results) - 20} more results")
    
    print("\n" + "="*80)

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Search ServiceNow for RHEL Repository links")
    parser.add_argument("--terms", nargs="+", default=['RHEL', 'repo'],
                       help="Search terms (default: RHEL repo)")
    parser.add_argument("--output", choices=['json', 'csv', 'both'], default='both',
                       help="Output format (default: both)")
    parser.add_argument("--url", default=SERVICENOW_BASE,
                       help=f"ServiceNow base URL (default: {SERVICENOW_BASE})")
    
    args = parser.parse_args()
    
    # Perform search
    results = await search_servicenow_rhel_repo(search_terms=args.terms, base_url=args.url)
    
    # Print summary
    print_results_summary(results)
    
    # Save results
    if args.output in ['json', 'both']:
        save_results(results, 'json')
    if args.output in ['csv', 'both']:
        save_results(results, 'csv')
    
    print("\n✅ Search complete!")

if __name__ == '__main__':
    asyncio.run(main())
