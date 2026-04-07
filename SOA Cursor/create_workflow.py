#!/usr/bin/env python3
"""
Manual execution workflow for SOA data extraction
Guides user through manual extraction process
"""

import json
import pandas as pd
import os
from datetime import datetime

def load_stis():
    """Load STI list"""
    try:
        with open('soa_stis_list.json', 'r') as f:
            data = json.load(f)
            return data.get('stis', [])
    except FileNotFoundError:
        print("⚠️  Warning: soa_stis_list.json not found")
        return []

def get_csv_status():
    """Get status of CSV extraction"""
    try:
        df = pd.read_csv('soa_data_all_stis.csv')
        total = len(df)
        extracted = len(df[df['Status'].str.contains('Extracted', na=False)])
        pending = total - extracted
        return total, extracted, pending
    except FileNotFoundError:
        return 0, 0, 0

def create_workflow_guide():
    """Create workflow guide"""
    stis = load_stis()
    total, extracted, pending = get_csv_status()
    
    guide = f"""
{'='*80}
MANUAL EXECUTION WORKFLOW FOR SOA DATA EXTRACTION
{'='*80}

📊 Current Status:
   Total STIs: {len(stis)}
   Extracted: {extracted}
   Pending: {pending}

📋 Step-by-Step Process:

1. PREPARATION
   ✅ JavaScript extraction script ready: execute_extraction.js
   ✅ CSV file ready: soa_data_all_stis.csv
   ✅ Console output processor ready: process_console_output.py

2. FOR EACH STI:

   a) Navigate to ServiceNow Business Application page:
      URL Pattern: https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=<SYS_ID>
      
      To find sys_id:
      - Search for STI in ServiceNow Business Applications list
      - Click on the application
      - Copy sys_id from URL

   b) Open Browser Console (F12 or Right-click > Inspect > Console)

   c) Click on "Compliance" tab (if not already active)

   d) Copy and paste the JavaScript extraction code:
      File: execute_extraction.js
      
      Or run this simplified version:
      
      (function() {{
          var results = {{}};
          
          // Application Name
          var nameEl = document.querySelector('h1, h2, [role="heading"]');
          results.applicationName = nameEl ? (nameEl.textContent || '').trim() : 'empty value';
          
          // Criticality Tier
          var critEl = document.querySelector('select[name*="criticality" i], input[name*="criticality" i]');
          if (critEl) {{
              results.criticalityTier = critEl.value || (critEl.selectedOptions && critEl.selectedOptions[0]?.text) || 'empty value';
          }} else {{
              results.criticalityTier = 'empty value';
          }}
          
          // ESS URL (Compliance tab)
          var essEl = document.querySelector('input[name*="ess"][name*="url" i], a[name*="ess"][name*="url" i]');
          results.essUrl = essEl ? (essEl.value || essEl.href || '').trim() : 'empty value';
          
          // PIA URL (Compliance tab)
          var piaEl = document.querySelector('input[name*="pia"][name*="url" i], a[name*="pia"][name*="url" i]');
          results.piaUrl = piaEl ? (piaEl.value || piaEl.href || '').trim() : 'empty value';
          
          // Switch to Data Privacy tab for DPQ
          var dpqTab = document.querySelector('[role="tab"][name*="Data Privacy" i]');
          if (dpqTab) dpqTab.click();
          
          // Wait a moment for tab to load, then extract DPQ
          setTimeout(function() {{
              var dpqEl = document.querySelector('select[name*="dpq" i]');
              if (dpqEl) {{
                  var val = dpqEl.value || (dpqEl.selectedOptions && dpqEl.selectedOptions[0]?.text) || '';
                  results.dpqComplete = (val && val !== '-- None --') ? val.trim() : 'empty value';
              }} else {{
                  results.dpqComplete = 'empty value';
              }}
              
              // Clean up
              for (var key in results) {{
                  if (!results[key] || results[key].trim() === '') {{
                      results[key] = 'empty value';
                  }}
              }}
              
              // Output results
              console.log('SOA_EXTRACTION_RESULTS:', JSON.stringify(results, null, 2));
              window.soaExtractionResults = results;
          }}, 1000);
          
          return results;
      }})();

   e) Copy the JSON output from console (look for SOA_EXTRACTION_RESULTS)

   f) Save JSON to a file or use process_console_output.py:
      
      Option 1: Save to file and process:
         python3 process_console_output.py --sti ATRO-001 --file console_output.json
      
      Option 2: Pipe directly:
         echo '{{"applicationName":"ATROPOS",...}}' | python3 process_console_output.py --sti ATRO-001
      
      Option 3: Use --json flag:
         python3 process_console_output.py --sti ATRO-001 --json '{{"applicationName":"ATROPOS",...}}'

3. VERIFICATION:
   Check updated CSV:
      python3 check_extraction_status.py

4. CONTINUE:
   Repeat steps 2a-2f for next STI

📋 STI List ({len(stis)} total):
"""
    
    # Add STI list
    for i, sti in enumerate(stis[:20], 1):  # Show first 20
        guide += f"   {i}. {sti}\n"
    if len(stis) > 20:
        guide += f"   ... and {len(stis) - 20} more\n"
    
    guide += f"""
💡 Tips:
   - Keep browser console open while navigating
   - Copy extraction script to clipboard for quick access
   - Process multiple STIs in batches
   - Verify CSV updates after each extraction

🚀 Quick Start:
   1. Navigate to first STI's ServiceNow page
   2. Open console (F12)
   3. Run extraction script
   4. Copy JSON output
   5. Run: python3 process_console_output.py --sti <STI> --json '<JSON>'
"""
    
    return guide

def main():
    guide = create_workflow_guide()
    print(guide)
    
    # Save to file
    with open('MANUAL_EXTRACTION_WORKFLOW.md', 'w') as f:
        f.write(guide)
    
    print(f"\n✅ Workflow guide saved to: MANUAL_EXTRACTION_WORKFLOW.md")

if __name__ == "__main__":
    main()




