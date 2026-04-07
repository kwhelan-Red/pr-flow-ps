
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
