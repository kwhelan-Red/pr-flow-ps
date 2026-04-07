// Automated extraction for all STIs
// This script should be run for each STI

function extractSOAFields() {
    var fields = {};
    
    // Application Name
    var nameEl = document.querySelector('h1, h2, [role="heading"]') || 
                 document.querySelector('input[name*="name" i]');
    fields.applicationName = nameEl ? (nameEl.textContent || nameEl.value || '').trim() : 'empty value';
    
    // Criticality Tier
    var critEl = document.querySelector('select[name*="criticality" i], input[name*="criticality" i]');
    if (critEl) {
        fields.criticalityTier = critEl.value || (critEl.selectedOptions && critEl.selectedOptions[0]?.text) || 'empty value';
    } else {
        fields.criticalityTier = 'empty value';
    }
    
    // ESS URL (need to be on Compliance tab)
    var essEl = document.querySelector('input[name*="ess"][name*="url" i], a[name*="ess"][name*="url" i]');
    fields.essUrl = essEl ? (essEl.value || essEl.href || '').trim() : 'empty value';
    
    // PIA URL (need to be on Compliance tab)
    var piaEl = document.querySelector('input[name*="pia"][name*="url" i], a[name*="pia"][name*="url" i]');
    fields.piaUrl = piaEl ? (piaEl.value || piaEl.href || '').trim() : 'empty value';
    
    // DPQ Complete (need to be on Data Privacy tab)
    var dpqEl = document.querySelector('select[name*="dpq" i]');
    if (dpqEl) {
        fields.dpqComplete = dpqEl.value || (dpqEl.selectedOptions && dpqEl.selectedOptions[0]?.text) || 'empty value';
    } else {
        fields.dpqComplete = 'empty value';
    }
    
    // Clean up
    for (var key in fields) {
        if (!fields[key] || fields[key] === '-- None --' || fields[key].trim() === '') {
            fields[key] = 'empty value';
        }
    }
    
    return fields;
}

// Execute and return
var results = extractSOAFields();
console.log('Extracted:', JSON.stringify(results, null, 2));
results;




