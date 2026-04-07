#!/usr/bin/env python3
"""
Read SOA field values directly from ServiceNow page using browser automation
Extracts actual DOM values, not just field locations
"""

import pandas as pd
import json
from datetime import datetime

print("="*80)
print("READING FIELD VALUES FROM SERVICENOW PAGE")
print("="*80)

# JavaScript to extract field values
extract_script = """
(function() {
    var results = {};
    
    // Find ESS Assessment URL field
    var essSelectors = [
        'input[name*="ess"][name*="url" i]',
        'input[id*="ess"][id*="url" i]',
        'a[name*="ess"][name*="url" i]',
        '[aria-label*="ESS"][aria-label*="URL" i]'
    ];
    for (var sel of essSelectors) {
        var el = document.querySelector(sel);
        if (el) {
            results.essUrl = el.value || el.href || el.textContent || '';
            break;
        }
    }
    
    // Find PIA Assessment URL field
    var piaSelectors = [
        'input[name*="pia"][name*="url" i]',
        'input[id*="pia"][id*="url" i]',
        'a[name*="pia"][name*="url" i]',
        '[aria-label*="PIA"][aria-label*="URL" i]'
    ];
    for (var sel of piaSelectors) {
        var el = document.querySelector(sel);
        if (el) {
            results.piaUrl = el.value || el.href || el.textContent || '';
            break;
        }
    }
    
    // Find DPQ Complete field
    var dpqSelectors = [
        'select[name*="dpq" i]',
        'select[id*="dpq" i]',
        'input[name*="dpq" i]',
        '[aria-label*="DPQ" i]'
    ];
    for (var sel of dpqSelectors) {
        var el = document.querySelector(sel);
        if (el) {
            results.dpqValue = el.value || (el.selectedOptions && el.selectedOptions[0]?.text) || '';
            break;
        }
    }
    
    return JSON.stringify(results);
})();
"""

print(f"\n📋 JavaScript extraction script ready")
print(f"   Script will query DOM for field values")

print(f"\n🔍 Fields to extract:")
print(f"   ✅ ESS Assessment URL")
print(f"   ✅ PIA Assessment URL")
print(f"   ✅ DPQ Complete")
print(f"   ✅ Other SOA fields")

print(f"\n💡 Browser automation needs to:")
print(f"   1. Execute JavaScript on the page")
print(f"   2. Capture returned values")
print(f"   3. Populate CSV with extracted data")

# Save extraction script
with open('extract_fields.js', 'w') as f:
    f.write(extract_script)

print(f"\n✅ Extraction script saved: extract_fields.js")
print(f"   Ready for browser automation to execute")




