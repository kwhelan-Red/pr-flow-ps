#!/usr/bin/env python3
"""
Browser automation integration using Playwright
Supports JavaScript execution and return value capture
"""

import asyncio
import json
import pandas as pd
from datetime import datetime
import sys
import argparse

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
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

def load_extraction_script():
    """Load JavaScript extraction script"""
    try:
        with open('execute_extraction.js', 'r') as f:
            return f.read()
    except FileNotFoundError:
        # Fallback to inline script
        return """
(function() {
    var results = {};
    
    // Application Name
    var nameEl = document.querySelector('h1, h2, [role="heading"]');
    if (nameEl) {
        var nameText = nameEl.textContent || nameEl.innerText || '';
        results.applicationName = nameText.trim() || 'empty value';
    } else {
        results.applicationName = 'empty value';
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

async def wait_for_authentication(page, timeout=300):
    """Wait for user to complete SSO authentication"""
    print("🔐 Checking authentication status...")
    
    # Check if we're on a login/SSO page
    current_url = page.url
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
    
    # Check if we're on ServiceNow main page (authenticated)
    if 'redhat.service-now.com' in page.url:
        print("✅ Already authenticated or on ServiceNow page")
        return True
    
    return True

async def extract_with_playwright(url, js_script):
    """Extract values using Playwright"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print(f"🌐 Navigating to: {url}")
            await page.goto(url, wait_until='networkidle', timeout=60000)
            
            # Wait for authentication if needed
            await wait_for_authentication(page)
            
            # Wait for page to load
            await page.wait_for_timeout(2000)
            
            # Click Compliance tab if needed
            try:
                compliance_tab = page.locator('[role="tab"]:has-text("Compliance")')
                if await compliance_tab.count() > 0:
                    await compliance_tab.click()
                    await page.wait_for_timeout(1000)
            except:
                print("⚠️  Could not click Compliance tab, continuing...")
            
            # Execute extraction script
            print("🔍 Executing extraction script...")
            results = await page.evaluate(js_script)
            
            await browser.close()
            return results
        except Exception as e:
            await browser.close()
            raise e

def extract_with_selenium(url, js_script):
    """Extract values using Selenium"""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print(f"🌐 Navigating to: {url}")
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Click Compliance tab if needed
        try:
            compliance_tab = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[@role='tab' and contains(text(), 'Compliance')]"))
            )
            compliance_tab.click()
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            print("⚠️  Could not click Compliance tab, continuing...")
        
        # Execute extraction script
        print("🔍 Executing extraction script...")
        results = driver.execute_script(f"return {js_script}")
        
        return results
    finally:
        driver.quit()

def update_csv(csv_file, sti, results):
    """Update CSV with extracted results"""
    df = pd.read_csv(csv_file)
    
    if sti not in df['STI'].values:
        print(f"⚠️  Warning: STI {sti} not found in CSV")
        return False
    
    idx = df[df['STI'] == sti].index[0]
    
    column_mapping = {
        'applicationName': 'Application Name',
        'criticalityTier': 'Criticality Tier',
        'essUrl': 'ESS Assessment URL',
        'piaUrl': 'PIA Assessment URL',
        'dpqComplete': 'DPQ Complete'
    }
    
    updated_fields = []
    for js_key, csv_col in column_mapping.items():
        if js_key in results:
            value = results[js_key]
            if not value or value.strip() == '' or value == '-- None --':
                value = 'empty value'
            df.at[idx, csv_col] = value
            updated_fields.append(csv_col)
    
    df.at[idx, 'Status'] = 'Extracted via Automation'
    df.at[idx, 'Collection Date'] = datetime.now().isoformat()
    
    df.to_csv(csv_file, index=False)
    
    print(f"✅ Updated {sti}: {len(updated_fields)} fields")
    return True

async def extract_all_stis_playwright(stis, csv_file, base_url_template):
    """Extract all STIs using Playwright"""
    js_script = load_extraction_script()
    
    for sti in stis:
        # Construct URL - you'll need to get sys_id for each STI
        # For now, using a placeholder
        url = f"{base_url_template}?sys_id=<SYS_ID>"
        
        print(f"\n{'='*80}")
        print(f"Extracting: {sti}")
        print(f"{'='*80}")
        
        try:
            # Note: You'll need to get the actual sys_id for each STI
            # This is a placeholder - you'd need to search ServiceNow first
            print(f"⚠️  Need sys_id for {sti} - skipping for now")
            continue
            
            # Uncomment when you have sys_id:
            # results = await extract_with_playwright(url, js_script)
            # update_csv(csv_file, sti, results)
        except Exception as e:
            print(f"❌ Error extracting {sti}: {e}")
            continue

def main():
    parser = argparse.ArgumentParser(description="Extract SOA data using browser automation")
    parser.add_argument("--method", choices=['playwright', 'selenium'], default='playwright',
                        help="Browser automation method")
    parser.add_argument("--csv", default="soa_data_all_stis.csv", help="CSV file to update")
    parser.add_argument("--sti", help="Single STI to extract")
    parser.add_argument("--url", help="ServiceNow URL for STI")
    parser.add_argument("--all", action='store_true', help="Extract all STIs (requires sys_id mapping)")
    
    args = parser.parse_args()
    
    print("="*80)
    print("BROWSER AUTOMATION INTEGRATION")
    print("="*80)
    
    if args.method == 'playwright':
        if not PLAYWRIGHT_AVAILABLE:
            print("❌ Error: Playwright not installed")
            print("   Install with: pip install playwright")
            print("   Then run: playwright install chromium")
            sys.exit(1)
        
        if args.sti and args.url:
            js_script = load_extraction_script()
            asyncio.run(extract_with_playwright(args.url, js_script))
        elif args.all:
            # Load STIs
            try:
                with open('soa_stis_list.json', 'r') as f:
                    data = json.load(f)
                    stis = data.get('stis', [])
            except FileNotFoundError:
                print("❌ Error: soa_stis_list.json not found")
                sys.exit(1)
            
            base_url = "https://redhat.service-now.com/cmdb_ci_business_app.do"
            asyncio.run(extract_all_stis_playwright(stis, args.csv, base_url))
        else:
            print("❌ Error: Need --sti and --url, or --all")
            sys.exit(1)
    
    elif args.method == 'selenium':
        if not SELENIUM_AVAILABLE:
            print("❌ Error: Selenium not installed")
            print("   Install with: pip install selenium")
            sys.exit(1)
        
        if args.sti and args.url:
            js_script = load_extraction_script()
            results = extract_with_selenium(args.url, js_script)
            update_csv(args.csv, args.sti, results)
        else:
            print("❌ Error: Need --sti and --url")
            sys.exit(1)

if __name__ == "__main__":
    main()


