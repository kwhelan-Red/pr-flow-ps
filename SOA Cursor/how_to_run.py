#!/usr/bin/env python3
"""
Simple step-by-step guide for running SOA extraction scripts
"""

print("="*80)
print("HOW TO RUN SOA EXTRACTION SCRIPTS - STEP BY STEP")
print("="*80)

print("""
📋 METHOD 1: Manual Console Extraction (Easiest to Start)

STEP 1: Get JSON from Browser Console
---------------------------------------
1. Open ServiceNow page for an STI (e.g., ATRO-001)
   URL: https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=0057625a1be086101fbd64e9bc4bcbc4

2. Press F12 to open browser console

3. Click the "Compliance" tab on the page

4. Copy and paste this JavaScript code into the console:

(function() {
    var results = {};
    var nameEl = document.querySelector('h1, h2, [role="heading"]');
    results.applicationName = nameEl ? (nameEl.textContent || '').trim() : 'empty value';
    var critEl = document.querySelector('select[name*="criticality" i], input[name*="criticality" i]');
    if (critEl) {
        results.criticalityTier = critEl.value || (critEl.selectedOptions && critEl.selectedOptions[0]?.text) || 'empty value';
    } else {
        results.criticalityTier = 'empty value';
    }
    var essEl = document.querySelector('input[name*="ess"][name*="url" i], a[name*="ess"][name*="url" i]');
    results.essUrl = essEl ? (essEl.value || essEl.href || '').trim() : 'empty value';
    var piaEl = document.querySelector('input[name*="pia"][name*="url" i], a[name*="pia"][name*="url" i]');
    results.piaUrl = piaEl ? (piaEl.value || piaEl.href || '').trim() : 'empty value';
    for (var key in results) {
        if (!results[key] || results[key].trim() === '') {
            results[key] = 'empty value';
        }
    }
    console.log('SOA_RESULTS:', JSON.stringify(results, null, 2));
    return results;
})();

5. Press Enter

6. Look for output that starts with: SOA_RESULTS:
   Copy the entire JSON object (everything between { and })

STEP 2: Run the Processing Script
----------------------------------
Open Terminal and run:

cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"

Then run this command (replace the JSON with what you copied):

python3 process_console_output.py --sti ATRO-001 --json '{"applicationName":"ATROPOS","criticalityTier":"C1","essUrl":"empty value","piaUrl":"empty value"}'

STEP 3: Check if it worked
---------------------------
python3 check_extraction_status.py

You should see ATRO-001 listed as extracted!


📋 METHOD 2: Save JSON to File (Easier for Multiple STIs)

STEP 1: Save JSON to a file
-----------------------------
1. After getting JSON from console, save it to a file:
   
   Create a folder:
   mkdir -p console_outputs
   
   Save JSON to file (replace with your actual JSON):
   echo '{"applicationName":"ATROPOS","criticalityTier":"C1","essUrl":"empty value","piaUrl":"empty value"}' > console_outputs/ATRO-001.json

STEP 2: Process the file
-------------------------
python3 process_console_output.py --sti ATRO-001 --file console_outputs/ATRO-001.json

STEP 3: Check status
--------------------
python3 check_extraction_status.py


📋 METHOD 3: Interactive Mode (Easiest for Copy-Paste)

STEP 1: Run interactive mode
----------------------------
python3 process_console_output.py --sti ATRO-001

STEP 2: Paste your JSON
-----------------------
Paste the JSON you copied from console, then press:
- Mac/Linux: Ctrl+D
- Windows: Ctrl+Z then Enter


💡 TROUBLESHOOTING

Problem: "command not found: python3"
Solution: Try "python" instead of "python3"

Problem: "No such file or directory"
Solution: Make sure you're in the right folder:
  cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"

Problem: "Could not parse JSON"
Solution: Make sure you copied the entire JSON object including { and }

Problem: "STI not found in CSV"
Solution: Check the STI name matches exactly (case-sensitive)


🚀 QUICK TEST

Let's test with a sample JSON:

python3 process_console_output.py --sti ATRO-001 --json '{"applicationName":"ATROPOS","criticalityTier":"C1","essUrl":"empty value","piaUrl":"empty value","dpqComplete":"empty value"}'

Then check:
python3 check_extraction_status.py
""")

print("\n" + "="*80)
print("Ready to start? Follow the steps above!")
print("="*80)




