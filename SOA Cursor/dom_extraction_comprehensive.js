
// Comprehensive DOM extraction for ServiceNow SOA fields
(function() {
    var extractValue = function(selectors, isSelect = false) {
        for (var sel of selectors) {
            var el = document.querySelector(sel);
            if (el) {
                if (isSelect) {
                    return el.value || (el.selectedOptions && el.selectedOptions[0]?.text) || 'empty value';
                } else {
                    return el.value || el.href || el.textContent || 'empty value';
                }
            }
        }
        return 'empty value';
    };
    
    var results = {
        applicationName: extractValue([
            'h1', 'h2', '[role="heading"]',
            'input[name*="name" i]',
            'input[id*="name" i]'
        ]),
        criticalityTier: extractValue([
            'select[name*="criticality" i]',
            'select[id*="criticality" i]',
            'input[name*="criticality" i]'
        ], true),
        essUrl: extractValue([
            'input[name*="ess"][name*="url" i]',
            'input[id*="ess"][id*="url" i]',
            'a[name*="ess"][name*="url" i]'
        ]),
        piaUrl: extractValue([
            'input[name*="pia"][name*="url" i]',
            'input[id*="pia"][id*="url" i]',
            'a[name*="pia"][name*="url" i]'
        ]),
        dpqComplete: extractValue([
            'select[name*="dpq" i]',
            'select[id*="dpq" i]'
        ], true),
        soaApplicable: extractValue([
            'input[name*="soa_applicable" i]',
            'input[id*="soa_applicable" i]',
            'input[type="checkbox"][name*="soa" i]'
        ]),
        installStatus: extractValue([
            'select[name*="install_status" i]',
            'select[id*="install_status" i]'
        ], true),
        dataClassification: extractValue([
            'select[name*="classification" i]',
            'select[id*="classification" i]'
        ], true)
    };
    
    // Clean up values
    for (var key in results) {
        if (!results[key] || results[key].trim() === '' || results[key] === '-- None --') {
            results[key] = 'empty value';
        } else {
            results[key] = results[key].trim();
        }
    }
    
    console.log('Extracted Values:', JSON.stringify(results, null, 2));
    return results;
})();
