// Run this in browser console on ServiceNow page
// Empty values will be marked as 'empty value'
(function() {
    var results = {};
    
    // ESS URL
    var essSelectors = [
        'input[name*="ess"][name*="url" i]',
        'input[id*="ess"][id*="url" i]',
        'input[name*="u_ess_url"]',
        'input[id*="u_ess_url"]'
    ];
    var essFound = false;
    for (var sel of essSelectors) {
        var el = document.querySelector(sel);
        if (el) {
            results.essUrl = el.value && el.value.trim() ? el.value.trim() : 'empty value';
            essFound = true;
            break;
        }
    }
    if (!essFound) results.essUrl = 'empty value';
    
    // PIA URL
    var piaSelectors = [
        'input[name*="pia"][name*="url" i]',
        'input[id*="pia"][id*="url" i]',
        'input[name*="u_pia_url"]',
        'input[id*="u_pia_url"]'
    ];
    var piaFound = false;
    for (var sel of piaSelectors) {
        var el = document.querySelector(sel);
        if (el) {
            results.piaUrl = el.value && el.value.trim() ? el.value.trim() : 'empty value';
            piaFound = true;
            break;
        }
    }
    if (!piaFound) results.piaUrl = 'empty value';
    
    // DPQ Complete
    var dpqSelectors = [
        'select[name*="dpq" i]',
        'select[id*="dpq" i]',
        'select[name*="u_dpq_complete"]',
        'select[id*="u_dpq_complete"]'
    ];
    var dpqFound = false;
    for (var sel of dpqSelectors) {
        var el = document.querySelector(sel);
        if (el) {
            var value = el.value || (el.selectedOptions[0]?.text || '');
            results.dpqComplete = value && value.trim() && value !== '-- None --' ? value.trim() : 'empty value';
            dpqFound = true;
            break;
        }
    }
    if (!dpqFound) results.dpqComplete = 'empty value';
    
    console.log('Extracted Values:', JSON.stringify(results, null, 2));
    return results;
})();
