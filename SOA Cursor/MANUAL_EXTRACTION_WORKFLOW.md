
================================================================================
MANUAL EXECUTION WORKFLOW FOR SOA DATA EXTRACTION
================================================================================

📊 Current Status:
   Total STIs: 114
   Extracted: 0
   Pending: 114

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
      
      (function() {
          var results = {};
          
          // Application Name
          var nameEl = document.querySelector('h1, h2, [role="heading"]');
          results.applicationName = nameEl ? (nameEl.textContent || '').trim() : 'empty value';
          
          // Criticality Tier
          var critEl = document.querySelector('select[name*="criticality" i], input[name*="criticality" i]');
          if (critEl) {
              results.criticalityTier = critEl.value || (critEl.selectedOptions && critEl.selectedOptions[0]?.text) || 'empty value';
          } else {
              results.criticalityTier = 'empty value';
          }
          
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
          setTimeout(function() {
              var dpqEl = document.querySelector('select[name*="dpq" i]');
              if (dpqEl) {
                  var val = dpqEl.value || (dpqEl.selectedOptions && dpqEl.selectedOptions[0]?.text) || '';
                  results.dpqComplete = (val && val !== '-- None --') ? val.trim() : 'empty value';
              } else {
                  results.dpqComplete = 'empty value';
              }
              
              // Clean up
              for (var key in results) {
                  if (!results[key] || results[key].trim() === '') {
                      results[key] = 'empty value';
                  }
              }
              
              // Output results
              console.log('SOA_EXTRACTION_RESULTS:', JSON.stringify(results, null, 2));
              window.soaExtractionResults = results;
          }, 1000);
          
          return results;
      })();

   e) Copy the JSON output from console (look for SOA_EXTRACTION_RESULTS)

   f) Save JSON to a file or use process_console_output.py:
      
      Option 1: Save to file and process:
         python3 process_console_output.py --sti ATRO-001 --file console_output.json
      
      Option 2: Pipe directly:
         echo '{"applicationName":"ATROPOS",...}' | python3 process_console_output.py --sti ATRO-001
      
      Option 3: Use --json flag:
         python3 process_console_output.py --sti ATRO-001 --json '{"applicationName":"ATROPOS",...}'

3. VERIFICATION:
   Check updated CSV:
      python3 check_extraction_status.py

4. CONTINUE:
   Repeat steps 2a-2f for next STI

📋 STI List (114 total):
   1. AAP-001
   2. ANSI-001
   3. ARR-002
   4. ARR-007
   5. ASRE-001
   6. ASRE-002
   7. ASRE-005
   8. ASRE-013
   9. ASSH-001
   10. ATLA-001
   11. BADG-001
   12. BEAK-001
   13. BOTA-001
   14. BREW-001
   15. CGER-001
   16. CHAR-001
   17. CICA-001
   18. CIRP-001
   19. CLIO-001
   20. COMP-016
   ... and 94 more

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
