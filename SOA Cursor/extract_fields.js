
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
