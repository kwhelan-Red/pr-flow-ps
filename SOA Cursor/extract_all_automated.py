#!/usr/bin/env python3
"""
Automated SOA Data Extraction for All STIs
Uses browser automation to extract data from ServiceNow
"""

import asyncio
import json
import pandas as pd
from datetime import datetime
import sys
import os

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

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
    
    // DPQ Complete - Data Privacy tab
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

def save_progress(sti, results, status_file='extraction_progress.json'):
    """Save extraction progress"""
    try:
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                progress = json.load(f)
        else:
            progress = {'extracted': {}, 'failed': []}
        
        progress['extracted'][sti] = {
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(status_file, 'w') as f:
            json.dump(progress, f, indent=2)
    except Exception as e:
        print(f"⚠️  Warning: Could not save progress: {e}")

async def wait_for_authentication(page, timeout=300):
    """Wait for user to complete SSO authentication - only if actually needed"""
    # Wait a moment for page to load
    await page.wait_for_timeout(2000)
    
    current_url = page.url
    
    # Check if we're on a login/SSO page
    is_login_page = ('login' in current_url.lower() or 
                     'sso' in current_url.lower() or 
                     'auth' in current_url.lower() or
                     'saml' in current_url.lower())
    
    # Also check page content for login indicators
    if not is_login_page:
        try:
            page_content = await page.content()
            is_login_page = ('sign in' in page_content.lower() or 
                           'log in' in page_content.lower() or
                           'authentication' in page_content.lower() or
                           'sso' in page_content.lower())
        except:
            pass
    
    if is_login_page:
        print("⚠️  Authentication required!")
        print("   Please complete SSO login in the browser window.")
        print("   Waiting for authentication to complete (max 5 minutes)...")
        
        # Wait for URL to change away from login page
        try:
            await page.wait_for_function(
                "() => { const url = window.location.href.toLowerCase(); return !url.includes('login') && !url.includes('sso') && !url.includes('auth') && !url.includes('saml'); }",
                timeout=timeout * 1000
            )
            print("✅ Authentication detected!")
            await page.wait_for_timeout(3000)  # Wait for page to fully load
        except Exception as e:
            print(f"⚠️  Authentication timeout or error: {e}")
            print("   Continuing anyway - authentication may have completed")
            await page.wait_for_timeout(3000)
    else:
        # Already authenticated - cookies are working
        pass
    
    return True

async def extract_with_playwright(sti, page=None, context=None, base_url="https://redhat.service-now.com"):
    """Extract data using Playwright with persistent browser context - reuses existing page"""
    if not PLAYWRIGHT_AVAILABLE:
        return None
    
    if context is None:
        raise ValueError("context must be provided")
    
    if page is None:
        # Use existing page if available, otherwise create new one
        page = context.pages[0] if context.pages else await context.new_page()
    
    # First, search for the STI on the existing Business Applications list page
    search_url = f"{base_url}/cmdb_ci_business_app_list.do?sysparm_query=nameLIKE{sti}"
    
    try:
        print(f"🔍 Searching for {sti}...")
        
        # Navigate the existing page to search URL (reuse same tab)
        # Cookies from persistent context will be used automatically
        await page.goto(search_url, wait_until='networkidle', timeout=60000)
        
        # Quick check: if redirected to login, cookies may have expired
        # But this should NOT happen if persistent context is working
        current_url = page.url
        if 'login' in current_url.lower() or 'sso' in current_url.lower():
            print(f"⚠️  {sti}: Unexpected login redirect - cookies may have expired")
            print("   This should be rare with persistent sessions")
            # Don't wait for auth here - user already authenticated once
            # Just skip this STI or continue anyway
        
        await page.wait_for_timeout(2000)
        
        # Try to find and click the STI in the list
        try:
            # Look for link containing the STI
            sti_link = page.locator(f'a:has-text("{sti}")').first
            if await sti_link.count() > 0:
                print(f"   Clicking {sti} link...")
                await sti_link.click()
                # Wait for navigation to detail page
                await page.wait_for_load_state('networkidle', timeout=10000)
                await page.wait_for_timeout(3000)  # Extra wait for page to fully render
                
                # Verify we're on detail page (not list page)
                current_url = page.url
                if 'cmdb_ci_business_app.do' in current_url and 'sysparm_query' not in current_url:
                    print(f"   ✅ On detail page for {sti}")
                else:
                    print(f"   ⚠️  May still be on list page, waiting more...")
                    await page.wait_for_timeout(3000)
            else:
                print(f"⚠️  {sti} not found in search results")
                # Navigate back to list page for next search
                await page.goto(f"{base_url}/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=30000)
                return None
        except Exception as e:
            print(f"⚠️  Could not find {sti} link: {e}")
            # Navigate back to list page for next search
            await page.goto(f"{base_url}/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=30000)
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
                print(f"   ✅ Clicked Compliance tab")
            else:
                print(f"   ⚠️  Compliance tab not found, continuing anyway...")
        except Exception as e:
            print(f"   ⚠️  Could not click Compliance tab: {e}")
        
        # Execute extraction script - verify we're extracting from detail page
        print(f"📊 Extracting data for {sti}...")
        
        # Double-check we're on detail page before extracting
        page_url = await page.evaluate("window.location.href")
        if 'sysparm_query' in page_url:
            print(f"   ⚠️  Still on list page! Cannot extract. URL: {page_url}")
            # Navigate back to list page for next search
            await page.goto(f"{base_url}/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=30000)
            return None
        
        results = await page.evaluate(EXTRACTION_SCRIPT)
        
        # Verify extraction got real data (not "Business Applications")
        if results and results.get('applicationName') == 'Business Applications':
            print(f"   ⚠️  Got list page title instead of app name - may need more wait time")
        
        # Don't close the page - keep it open to reuse for next STI
        # Navigate back to list page for next search
        await page.goto(f"{base_url}/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(1000)  # Brief wait for list page to load
        
        return results
            
    except Exception as e:
        print(f"❌ Error extracting {sti}: {e}")
        # Navigate back to list page for next search
        try:
            await page.goto(f"{base_url}/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=30000)
        except:
            pass
        return None

def extract_with_selenium(sti, base_url="https://redhat.service-now.com"):
    """Extract data using Selenium"""
    if not SELENIUM_AVAILABLE:
        return None
    
    options = Options()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        search_url = f"{base_url}/cmdb_ci_business_app_list.do?sysparm_query=nameLIKE{sti}"
        
        print(f"🔍 Searching for {sti}...")
        driver.get(search_url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Find and click STI link
        try:
            sti_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, sti))
            )
            sti_link.click()
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            print(f"⚠️  Could not find {sti} link")
            driver.quit()
            return None
        
        # Click Compliance tab
        try:
            compliance_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@role='tab' and contains(text(), 'Compliance')]"))
            )
            compliance_tab.click()
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            print(f"⚠️  Could not click Compliance tab for {sti}")
        
        # Execute extraction script
        print(f"📊 Extracting data for {sti}...")
        results = driver.execute_script(f"return {EXTRACTION_SCRIPT}")
        
        driver.quit()
        return results
        
    except Exception as e:
        print(f"❌ Error extracting {sti}: {e}")
        driver.quit()
        return None

def update_csv(sti, results):
    """Update CSV with extracted results"""
    try:
        from process_console_output import update_csv_with_results
        return update_csv_with_results('soa_data_all_stis.csv', sti, results)
    except Exception as e:
        print(f"❌ Error updating CSV for {sti}: {e}")
        return False

async def extract_all_stis_async(method='playwright', start_from=0, max_stis=None):
    """Extract all STIs asynchronously with persistent browser session"""
    stis = load_stis()
    
    if max_stis:
        stis = stis[start_from:start_from+max_stis]
    else:
        stis = stis[start_from:]
    
    print(f"🚀 Starting extraction for {len(stis)} STIs")
    print(f"   Method: {method}")
    print(f"   Starting from: {stis[0] if stis else 'N/A'}")
    print("="*80)
    
    extracted = 0
    failed = 0
    
    # Use persistent browser context for all STIs
    browser = None
    context = None
    
    if method == 'playwright' and PLAYWRIGHT_AVAILABLE:
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
            
            print("\n🌐 Browser opened - ONE window will stay open for all STIs")
            print("   Using persistent session (NOT private mode) - cookies will be saved")
            print("   🔐 Authenticating ONCE - session will be reused for all STIs\n")
            
            # Authenticate ONCE at the start - cookies will persist for all STIs
            auth_page = context.pages[0] if context.pages else await context.new_page()
            try:
                print("🔐 Checking authentication status...")
                await auth_page.goto("https://redhat.service-now.com/cmdb_ci_business_app_list.do", wait_until='networkidle', timeout=60000)
                
                # Wait for authentication if needed (ONLY ONCE)
                await wait_for_authentication(auth_page)
                
                # Verify we're authenticated by checking cookies
                cookies = await context.cookies()
                has_auth_cookie = any('servicenow' in c.get('domain', '').lower() or 'jsessionid' in c.get('name', '').lower() for c in cookies)
                
                if has_auth_cookie or 'redhat.service-now.com' in auth_page.url:
                    print("✅ Authentication verified! Cookies saved - will be reused for all STIs.\n")
                else:
                    print("⚠️  Note: If you see login prompts, complete authentication once.\n")
                
                # Don't close the auth page - keep it open so session persists
                # The persistent context will save cookies automatically
            except Exception as e:
                print(f"⚠️  Initial authentication check: {e}")
                print("   Continuing anyway - cookies may already be saved\n")
            
            # Use the auth page (already on Business Applications list) for all STI searches
            search_page = auth_page
            
            for i, sti in enumerate(stis, 1):
                print(f"\n[{i}/{len(stis)}] Processing {sti}...")
                
                try:
                    results = await extract_with_playwright(sti, page=search_page, context=context)
                    
                    if results:
                        if update_csv(sti, results):
                            save_progress(sti, results)
                            extracted += 1
                            print(f"✅ {sti}: Extracted successfully")
                        else:
                            failed += 1
                            print(f"❌ {sti}: Failed to update CSV")
                    else:
                        failed += 1
                        print(f"❌ {sti}: No data extracted")
                        
                except Exception as e:
                    failed += 1
                    print(f"❌ {sti}: Error - {e}")
                
                # Small delay between requests
                if i < len(stis):
                    await asyncio.sleep(2)
            
            # Close browser context at the end
            await context.close()
            print("\n🌐 Browser closed")
    else:
        # Fallback to non-persistent method (Selenium or no Playwright)
        for i, sti in enumerate(stis, 1):
            print(f"\n[{i}/{len(stis)}] Processing {sti}...")
            
            try:
                if method == 'playwright':
                    results = await extract_with_playwright(sti)
                else:
                    results = extract_with_selenium(sti)
                
                if results:
                    if update_csv(sti, results):
                        save_progress(sti, results)
                        extracted += 1
                        print(f"✅ {sti}: Extracted successfully")
                    else:
                        failed += 1
                        print(f"❌ {sti}: Failed to update CSV")
                else:
                    failed += 1
                    print(f"❌ {sti}: No data extracted")
                    
            except Exception as e:
                failed += 1
                print(f"❌ {sti}: Error - {e}")
            
            # Small delay between requests
            await asyncio.sleep(2)
    
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
    print(f"✅ Extracted: {extracted}")
    print(f"❌ Failed: {failed}")
    if extracted + failed > 0:
        print(f"📊 Success rate: {(extracted/(extracted+failed)*100):.1f}%")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated extraction for all STIs")
    parser.add_argument("--method", choices=['playwright', 'selenium'], default='playwright',
                        help="Browser automation method")
    parser.add_argument("--start-from", type=int, default=0, help="Start from STI index")
    parser.add_argument("--max", type=int, help="Maximum number of STIs to process")
    parser.add_argument("--install-playwright", action='store_true', 
                        help="Install Playwright browsers")
    
    args = parser.parse_args()
    
    if args.install_playwright:
        print("Installing Playwright browsers...")
        import subprocess
        subprocess.run(['playwright', 'install', 'chromium'])
        return
    
    if args.method == 'playwright' and not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright not installed")
        print("   Install with: pip install playwright")
        print("   Then run: playwright install chromium")
        print("   Or use: python3 extract_all_automated.py --install-playwright")
        return
    
    if args.method == 'selenium' and not SELENIUM_AVAILABLE:
        print("❌ Selenium not installed")
        print("   Install with: pip install selenium")
        return
    
    asyncio.run(extract_all_stis_async(args.method, args.start_from, args.max))

if __name__ == '__main__':
    main()


