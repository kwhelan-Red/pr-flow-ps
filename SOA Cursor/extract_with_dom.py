#!/usr/bin/env python3
"""
Extract SOA field values using DOM querying approach
Attempts to read values from ServiceNow page elements
"""

import pandas as pd
import json
from datetime import datetime
import re

print("="*80)
print("EXTRACTING VALUES USING DOM QUERYING")
print("="*80)

# Load CSV
df = pd.read_csv('soa_data_all_stis.csv')

print(f"\n📊 Current CSV: {len(df)} records")

# For ATROPOS (ATRO-001) - we're on this page
# Let's try to extract what we can from the page structure

print(f"\n🔍 Attempting to extract values from current page...")
print(f"   STI: ATRO-001 (ATROPOS)")

# JavaScript to extract values - this would need to be executed in browser
extraction_js = """
(function() {
    var results = {};
    
    // Try to find ESS URL field
    var essFields = document.querySelectorAll('input[type="text"], input[type="url"]');
    for (var field of essFields) {
        var label = field.closest('div')?.querySelector('label');
        if (label && (label.textContent.includes('ESS') || label.textContent.includes('Security')) 
            && label.textContent.includes('URL')) {
            results.essUrl = field.value || 'empty value';
            break;
        }
    }
    
    // Try to find PIA URL field
    for (var field of essFields) {
        var label = field.closest('div')?.querySelector('label');
        if (label && (label.textContent.includes('PIA') || label.textContent.includes('Privacy')) 
            && label.textContent.includes('URL')) {
            results.piaUrl = field.value || 'empty value';
            break;
        }
    }
    
    // Try to find DPQ Complete
    var selects = document.querySelectorAll('select');
    for (var select of selects) {
        var label = select.closest('div')?.querySelector('label');
        if (label && label.textContent.includes('DPQ')) {
            results.dpqComplete = select.value || select.selectedOptions[0]?.text || 'empty value';
            break;
        }
    }
    
    // Application Name from heading
    var heading = document.querySelector('h1, h2, [role="heading"]');
    if (heading) {
        results.applicationName = heading.textContent.trim() || 'empty value';
    }
    
    // Criticality Tier
    var criticalityFields = document.querySelectorAll('select, input');
    for (var field of criticalityFields) {
        var label = field.closest('div')?.querySelector('label');
        if (label && label.textContent.includes('Criticality')) {
            results.criticalityTier = field.value || (field.selectedOptions && field.selectedOptions[0]?.text) || 'empty value';
            break;
        }
    }
    
    return JSON.stringify(results);
})();
"""

print(f"\n📋 JavaScript extraction code ready")
print(f"   This needs to be executed in browser console")

# Save extraction script
with open('dom_extraction.js', 'w') as f:
    f.write(extraction_js)

print(f"\n✅ Extraction script saved: dom_extraction.js")
print(f"\n💡 To extract values:")
print(f"   1. Open browser console on ServiceNow page")
print(f"   2. Run: dom_extraction.js")
print(f"   3. Copy returned JSON")
print(f"   4. Update CSV with extracted values")

print(f"\n🚀 Attempting alternative extraction methods...")

EOF




