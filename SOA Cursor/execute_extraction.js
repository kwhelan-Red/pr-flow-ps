
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
    
    // Criticality Tier - try multiple selectors
    var critSelectors = [
        'select[name*="criticality" i]',
        'select[id*="criticality" i]',
        'input[name*="criticality" i]',
        '[aria-label*="criticality" i]'
    ];
    var critFound = false;
    for (var sel of critSelectors) {
        var el = document.querySelector(sel);
        if (el) {
            if (el.tagName === 'SELECT') {
                results.criticalityTier = el.value || (el.selectedOptions && el.selectedOptions[0]?.text) || 'empty value';
            } else {
                results.criticalityTier = el.value || 'empty value';
            }
            critFound = true;
            break;
        }
    }
    if (!critFound) results.criticalityTier = 'empty value';
    
    // ESS URL - Compliance tab
    var essSelectors = [
        'input[name*="ess"][name*="url" i]',
        'input[id*="ess"][id*="url" i]',
        'a[name*="ess"][name*="url" i]'
    ];
    var essFound = false;
    for (var sel of essSelectors) {
        var el = document.querySelector(sel);
        if (el) {
            results.essUrl = (el.value || el.href || '').trim() || 'empty value';
            essFound = true;
            break;
        }
    }
    if (!essFound) results.essUrl = 'empty value';
    
    // PIA URL - Compliance tab
    var piaSelectors = [
        'input[name*="pia"][name*="url" i]',
        'input[id*="pia"][id*="url" i]',
        'a[name*="pia"][name*="url" i]'
    ];
    var piaFound = false;
    for (var sel of piaSelectors) {
        var el = document.querySelector(sel);
        if (el) {
            results.piaUrl = (el.value || el.href || '').trim() || 'empty value';
            piaFound = true;
            break;
        }
    }
    if (!piaFound) results.piaUrl = 'empty value';
    
    // DPQ Complete - Data Privacy tab (need to switch tabs first)
    var dpqSelectors = [
        'select[name*="dpq" i]',
        'select[id*="dpq" i]'
    ];
    var dpqFound = false;
    for (var sel of dpqSelectors) {
        var el = document.querySelector(sel);
        if (el) {
            var value = el.value || (el.selectedOptions && el.selectedOptions[0]?.text) || '';
            results.dpqComplete = (value && value !== '-- None --') ? value.trim() : 'empty value';
            dpqFound = true;
            break;
        }
    }
    if (!dpqFound) results.dpqComplete = 'empty value';
    
    // Clean up empty values
    for (var key in results) {
        if (!results[key] || results[key] === '-- None --' || results[key].trim() === '') {
            results[key] = 'empty value';
        } else {
            results[key] = results[key].trim();
        }
    }
    
    // Output to console
    console.log('=== SOA FIELD EXTRACTION RESULTS ===');
    console.log(JSON.stringify(results, null, 2));
    
    // Also store in window for retrieval
    window.soaExtractionResults = results;
    
    return results;
})();
