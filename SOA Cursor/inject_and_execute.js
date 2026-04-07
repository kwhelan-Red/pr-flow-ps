
// Inject and execute extraction script
var script = document.createElement('script');
script.textContent = `(function() {
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
    
    // ESS URL
    var essEl = document.querySelector('input[name*="ess"][name*="url" i], a[name*="ess"][name*="url" i]');
    results.essUrl = essEl ? (essEl.value || essEl.href || '').trim() : 'empty value';
    
    // PIA URL
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
        if (!results[key] || results[key].trim() === '') {
            results[key] = 'empty value';
        }
    }
    
    // Store in window and log
    window.soaExtractionResults = results;
    console.log('SOA_EXTRACTION_RESULTS:', JSON.stringify(results));
    
    // Also create a visible element with results
    var div = document.createElement('div');
    div.id = 'soa-extraction-results';
    div.style.display = 'none';
    div.textContent = JSON.stringify(results);
    document.body.appendChild(div);
    
    return results;
})();`;
document.body.appendChild(script);
