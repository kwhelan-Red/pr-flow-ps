#!/usr/bin/env python3
"""
Simplified Automated Extraction - Test Version
Tests extraction on a few STIs first
"""

import asyncio
import json
import pandas as pd
from datetime import datetime
import sys
import os

# Check dependencies
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed")
    print("   Install: pip install --break-system-packages playwright")
    print("   Then: playwright install chromium")

# JavaScript extraction script
EXTRACTION_SCRIPT = """
(function() {
    var results = {};
    
    // Application Name - look for specific ServiceNow form field or heading
    // Try form field first (most reliable)
    var nameEl = document.querySelector('input[name*="name"][id*="name"], input[id*="u_name"], input[name*="u_name"]');
    if (nameEl && nameEl.value && nameEl.value.trim() !== '') {
        results.applicationName = nameEl.value.trim();
    } else {
        // Try heading, but exclude common page titles
        var headings = document.querySelectorAll('h1, h2, [role="heading"]');
        for (var h of headings) {
            var text = (h.textContent || h.innerText || '').trim();
            // Skip generic page titles
            if (text && 
                text !== 'Business Applications' && 
                text !== 'Application' &&
                text.length > 3 &&
                !text.includes('List') &&
                !text.includes('Search')) {
                results.applicationName = text;
                break;
            }
        }
        if (!results.applicationName) {
            results.applicationName = 'empty value';
        }
    }
    
    // Criticality Tier
    var critEl = document.querySelector('select[name*="criticality" i], input[name*="criticality" i]');
    if (critEl) {
        if (critEl.tagName === 'SELECT') {
            results.criticalityTier = critEl.value || (critEl.selectedOptions && critEl.selectedOptions[0]?.text) || 'empty value';
        } else {
            results.criticalityTier = critEl.value || 'empty value';
        }
    } else {
        results.criticalityTier = 'empty value';
    }
    
    // ESS URL - Compliance tab
    var essEl = document.querySelector('input[name*="ess"][name*="url" i], a[name*="ess"][name*="url" i]');
    results.essUrl = essEl ? (essEl.value || essEl.href || '').trim() : 'empty value';
    
    // PIA URL - Compliance tab
    var piaEl = document.querySelector('input[name*="pia"][name*="url" i], a[name*="pia"][name*="url" i]');
    results.piaUrl = piaEl ? (piaEl.value || piaEl.href || '').trim() : 'empty value';
    
    // DPQ Complete
    var dpqEl = document.querySelector('select[name*="dpq" i]');
    if (dpqEl) {
        var val = dpqEl.value || (dpqEl.selectedOptions && dpqEl.selectedOptions[0]?.text) || '';
        results.dpqComplete = (val && val !== '-- None --') ? val.trim() : 'empty value';
    } else {
        results.dpqComplete = 'empty value';
    }
    
    // Clean up
    for (var key in results) {
        if (!results[key] || results[key] === '-- None --' || results[key].trim() === '') {
            results[key] = 'empty value';
        } else {
            results[key] = results[key].trim();
        }
    }
    
    return results;
})();
"""

def load_stis():
    """Load all STIs from CSV"""
    try:
        df = pd.read_csv('soa_data_all_stis.csv')
        return df['STI'].tolist()
    except FileNotFoundError:
        print("❌ Error: soa_data_all_stis.csv not found")
        return []

def update_csv(sti, results):
    """Update CSV with extracted results"""
    try:
        from process_console_output import update_csv_with_results
        return update_csv_with_results('soa_data_all_stis.csv', sti, results)
    except Exception as e:
        print(f"❌ Error updating CSV for {sti}: {e}")
        return False

async def wait_for_authentication(page, timeout=300):
    """Wait for user to complete SSO authentication - only if actually needed"""
    # Quick check: if we're already on ServiceNow and not on login page, we're authenticated
    current_url = page.url
    
    # If already on ServiceNow main page (not login), skip check
    if 'redhat.service-now.com' in current_url and 'login' not in current_url.lower() and 'sso' not in current_url.lower() and 'auth' not in current_url.lower():
        # Check if page has ServiceNow content (not login form)
        try:
            # Quick check for ServiceNow UI elements
            has_servicenow_ui = await page.evaluate("""
                () => {
                    return document.querySelector('.navbar, .navpage, [id*="header"], .header') !== null ||
                           document.querySelector('body').innerText.includes('ServiceNow') ||
                           window.location.href.includes('redhat.service-now.com');
                }
            """)
            if has_servicenow_ui:
                return True  # Already authenticated, skip
        except:
            pass
    
    # Only check if we're actually on a login/SSO page
    if 'login' in current_url.lower() or 'sso' in current_url.lower() or 'auth' in current_url.lower():
        print("⚠️  Authentication required!")
        print("   Please complete SSO login in the browser window.")
        print("   Waiting for authentication to complete (max 5 minutes)...")
        
        # Wait for URL to change away from login page
        try:
            await page.wait_for_function(
                "() => !window.location.href.toLowerCase().includes('login') && !window.location.href.toLowerCase().includes('sso') && !window.location.href.toLowerCase().includes('auth')",
                timeout=timeout * 1000
            )
            print("✅ Authentication detected!")
            await page.wait_for_timeout(3000)  # Wait for page to fully load
        except Exception as e:
            print(f"⚠️  Authentication timeout or error: {e}")
            print("   Continuing anyway - authentication may have completed")
            await page.wait_for_timeout(3000)
    
    return True

async def extract_sti_playwright(sti, page=None, context=None, base_url="https://redhat.service-now.com"):
    """Extract data for a single STI using Playwright - reuses existing page"""
    if not PLAYWRIGHT_AVAILABLE:
        return None
    
    # Use provided context or create new one
    should_close_context = False
    if context is None:
        async with async_playwright() as p:
            # Use persistent user data directory to save cookies/sessions (NOT private mode)
            import tempfile
            import os
            user_data_dir = os.path.join(tempfile.gettempdir(), 'playwright_servicenow_session')
            os.makedirs(user_data_dir, exist_ok=True)
            
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=False,
                args=['--disable-blink-features=AutomationControlled']
            )
            should_close_context = True
    
    # Use existing page if provided, otherwise use first available page or create new
    if page is None:
        page = context.pages[0] if context.pages else await context.new_page()
    
    # Search URL - search by name containing STI
    search_url = f"{base_url}/cmdb_ci_business_app_list.do?sysparm_query=nameLIKE{sti}"
    
    try:
        print(f"🔍 [{sti}] Searching ServiceNow...")
        # Navigate existing page to search URL (reuse same tab)
        await page.goto(search_url, wait_until='networkidle', timeout=60000)
        
        # No authentication check here - already authenticated at start
        # Persistent context saves cookies, so we're already logged in
        
        await page.wait_for_timeout(3000)  # Wait for page to load
        
        # Try to find the STI link in the results table
        # ServiceNow uses various selectors - try multiple approaches
        sti_found = False
        
        # Method 1: Look for link with STI text
        try:
            sti_selector = f'a:has-text("{sti}")'
            await page.wait_for_selector(sti_selector, timeout=5000)
            print(f"   Clicking {sti} link...")
            await page.click(sti_selector)
            # Wait for navigation to detail page
            await page.wait_for_load_state('networkidle', timeout=10000)
            await page.wait_for_timeout(3000)  # Extra wait for page to fully render
            
            # Verify we're on detail page
            current_url = page.url
            if 'cmdb_ci_business_app.do' in current_url and 'sysparm_query' not in current_url:
                print(f"   ✅ On detail page for {sti}")
            else:
                print(f"   ⚠️  May still be on list page, waiting more...")
                await page.wait_for_timeout(3000)
            
            sti_found = True
            print(f"✅ [{sti}] Found and clicked STI link")
        except:
            pass
        
        # Method 2: Look in table rows
        if not sti_found:
            try:
                # Get all links and find one containing STI
                links = await page.query_selector_all('a')
                for link in links:
                    text = await link.inner_text()
                    if sti in text:
                        print(f"   Clicking {sti} link (Method 2)...")
                        await link.click()
                        # Wait for navigation to detail page
                        await page.wait_for_load_state('networkidle', timeout=10000)
                        await page.wait_for_timeout(3000)
                        
                        # Verify we're on detail page
                        current_url = page.url
                        if 'cmdb_ci_business_app.do' in current_url and 'sysparm_query' not in current_url:
                            print(f"   ✅ On detail page for {sti}")
                        else:
                            print(f"   ⚠️  May still be on list page, waiting more...")
                            await page.wait_for_timeout(3000)
                        
                        sti_found = True
                        print(f"✅ [{sti}] Found STI in table")
                        break
            except:
                pass
        
        if not sti_found:
            print(f"⚠️  [{sti}] STI not found in search results")
            # Navigate back to list page for next search
            await page.goto(f"{base_url}/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=30000)
            if should_close_context:
                await context.close()
            return None
        
        # Click Compliance tab - wait for it to be available
        try:
            print(f"   Looking for Compliance tab...")
            await page.wait_for_timeout(2000)  # Wait for tabs to load
            compliance_tab = page.locator('[role="tab"]:has-text("Compliance"), [role="tab"]:has-text("COMPLIANCE")')
            if await compliance_tab.count() > 0:
                await compliance_tab.first.click()
                await page.wait_for_load_state('networkidle', timeout=5000)
                await page.wait_for_timeout(2000)  # Wait for Compliance tab content to load
                print(f"✅ [{sti}] Clicked Compliance tab")
            else:
                print(f"   ⚠️  Compliance tab not found, continuing anyway...")
        except Exception as e:
            print(f"⚠️  [{sti}] Could not click Compliance tab: {e}")
        
        # Execute extraction script - verify we're extracting from detail page
        print(f"📊 [{sti}] Extracting data...")
        
        # Double-check we're on detail page before extracting
        page_url = await page.evaluate("window.location.href")
        if 'sysparm_query' in page_url:
            print(f"   ⚠️  Still on list page! Cannot extract. URL: {page_url}")
            # Navigate back to list page for next search
            await page.goto(f"{base_url}/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=30000)
            if should_close_context:
                await context.close()
            return None
        
        results = await page.evaluate(EXTRACTION_SCRIPT)
        
        # Verify extraction got real data (not "Business Applications")
        if results and results.get('applicationName') == 'Business Applications':
            print(f"   ⚠️  Got list page title instead of app name - may need more wait time")
        
        # Don't close the page - keep it open to reuse for next STI
        # Navigate back to list page for next search
        await page.goto(f"{base_url}/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(1000)  # Brief wait for list page to load
        
        if should_close_context:
            await context.close()
        print(f"✅ [{sti}] Extraction complete")
        return results
            
    except Exception as e:
        print(f"❌ [{sti}] Error: {e}")
        # Navigate back to list page for next search
        try:
            await page.goto(f"{base_url}/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=30000)
        except:
            pass
        if should_close_context:
            await context.close()
        return None

async def extract_all_stis_test(max_stis=5):
    """Test extraction on a few STIs with persistent browser session"""
    stis = load_stis()
    
    if not stis:
        print("❌ No STIs found in CSV")
        return
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not available")
        print("   Install: pip install --break-system-packages playwright")
        print("   Then: playwright install chromium")
        return
    
    test_stis = stis[:max_stis]
    print(f"🚀 Testing extraction on {len(test_stis)} STIs")
    print(f"   STIs: {', '.join(test_stis)}")
    print("="*80)
    
    extracted = 0
    failed = 0
    
    # Use persistent browser context for all STIs (NOT private mode)
    async with async_playwright() as p:
        # Use persistent user data directory to save cookies/sessions
        import tempfile
        import os
        user_data_dir = os.path.join(tempfile.gettempdir(), 'playwright_servicenow_session')
        os.makedirs(user_data_dir, exist_ok=True)
        
        context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )
        
        print("\n🌐 Browser opened - ONE window will stay open for all STIs")
        print("   Using persistent session (NOT private mode) - cookies will be saved")
        print("   🔐 Authenticating ONCE - session will be reused for all STIs\n")
        
        # Authenticate ONCE at the start - cookies will persist for all STIs
        page = context.pages[0] if context.pages else await context.new_page()
        try:
            print("🔐 Checking authentication status...")
            await page.goto("https://redhat.service-now.com/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=60000)
            
            # Check if we need to authenticate (only once)
            current_url = page.url
            if 'login' in current_url.lower() or 'sso' in current_url.lower() or 'auth' in current_url.lower():
                print("⚠️  Authentication required!")
                print("   Please complete SSO login in the browser window.")
                print("   This is the ONLY time you'll need to authenticate.\n")
                await wait_for_authentication(page)
                print("✅ Authentication complete! Session saved - will be reused for all STIs.\n")
            else:
                print("✅ Already authenticated! Using saved session.\n")
            
            # Keep the page open (don't close it) so cookies persist
            # The persistent context will save the cookies automatically
        except Exception as e:
            print(f"⚠️  Initial authentication check: {e}")
            print("   Continuing anyway - cookies may already be saved\n")
        
        # Use the auth page (already on Business Applications list) for all STI searches
        # Reuse the same page that's already on the Business Applications list
        search_page = page
        
        for i, sti in enumerate(test_stis, 1):
            print(f"\n[{i}/{len(test_stis)}] Processing {sti}...")
            
            try:
                results = await extract_sti_playwright(sti, page=search_page, context=context)
                
                if results:
                    if update_csv(sti, results):
                        extracted += 1
                        print(f"✅ {sti}: Success - {results.get('applicationName', 'N/A')}")
                    else:
                        failed += 1
                        print(f"❌ {sti}: Failed to update CSV")
                else:
                    failed += 1
                    print(f"❌ {sti}: No data extracted")
                    
            except Exception as e:
                failed += 1
                print(f"❌ {sti}: Error - {e}")
            
            # Delay between requests
            if i < len(test_stis):
                await asyncio.sleep(3)
        
        # Close browser context at the end
        await context.close()
        print("\n🌐 Browser closed")
    
    print("\n" + "="*80)
    print("TEST EXTRACTION COMPLETE")
    print("="*80)
    print(f"✅ Extracted: {extracted}/{len(test_stis)}")
    print(f"❌ Failed: {failed}/{len(test_stis)}")
    
    if extracted > 0:
        print("\n💡 Test successful! You can now run full extraction:")
        print("   python3 extract_all_automated.py --method playwright --max 10")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Test automated extraction")
    parser.add_argument("--max", type=int, default=5, help="Number of STIs to test")
    
    args = parser.parse_args()
    
    print("="*80)
    print("TESTING AUTOMATED EXTRACTION")
    print("="*80)
    print(f"\n📋 Will test on {args.max} STIs")
    print("💡 Browser will open - you may need to log into ServiceNow")
    print("="*80)
    print()
    
    asyncio.run(extract_all_stis_test(args.max))

if __name__ == '__main__':
    main()


