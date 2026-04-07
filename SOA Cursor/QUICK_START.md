# Quick Start Guide - How to Run the Scripts

## 🚀 Easiest Way to Start

### Step 1: Open Terminal
- Press `Cmd + Space` (Mac) or `Win + R` (Windows)
- Type "Terminal" and press Enter

### Step 2: Go to the Right Folder
Copy and paste this command:
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
```

### Step 3: Test with Sample Data
Copy and paste this entire command:
```bash
python3 process_console_output.py --sti ATRO-001 --json '{"applicationName":"ATROPOS","criticalityTier":"C1","essUrl":"empty value","piaUrl":"empty value","dpqComplete":"empty value"}'
```

You should see: `✅ Updated ATRO-001: 5 fields`

### Step 4: Check if it Worked
```bash
python3 check_extraction_status.py
```

---

## 📋 Real Workflow (When You Have Real Data)

### 1. Get JSON from Browser Console

**In ServiceNow:**
1. Go to: https://redhat.service-now.com/cmdb_ci_business_app.do?sys_id=0057625a1be086101fbd64e9bc4bcbc4
2. Press **F12** (opens console)
3. Click **"Compliance"** tab
4. Paste this code and press Enter:

```javascript
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
```

5. **Copy the JSON output** (looks like: `{"applicationName":"ATROPOS",...}`)

### 2. Process the JSON

**In Terminal:**
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 process_console_output.py --sti ATRO-001 --json 'PASTE_YOUR_JSON_HERE'
```

Replace `PASTE_YOUR_JSON_HERE` with the JSON you copied.

### 3. Verify
```bash
python3 check_extraction_status.py
```

---

## 💡 Common Issues

**"python3: command not found"**
- Try: `python` instead of `python3`
- Or: `python3.9` or `python3.10`

**"No such file or directory"**
- Make sure you're in the right folder:
  ```bash
  cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
  pwd  # Should show: /Users/kwhelan/pr-flow-ps/SOA Cursor
  ```

**"Could not parse JSON"**
- Make sure you copied the entire JSON including `{` and `}`
- JSON should look like: `{"applicationName":"ATROPOS",...}`

**"STI not found"**
- Check the STI name matches exactly (case-sensitive)
- List all STIs: `grep "STI" soa_data_all_stis.csv | head -5`

---

## 🎯 Example Commands

**Test with sample data:**
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 process_console_output.py --sti ATRO-001 --json '{"applicationName":"ATROPOS","criticalityTier":"C1","essUrl":"empty value","piaUrl":"empty value","dpqComplete":"empty value"}'
```

**Check status:**
```bash
python3 check_extraction_status.py
```

**View workflow guide:**
```bash
python3 how_to_run.py
```

---

## 📞 Need Help?

1. Run: `python3 how_to_run.py` - Shows detailed guide
2. Check: `COMPLETE_WORKFLOW_GUIDE.md` - Full documentation
3. Test first: Use the sample JSON above to make sure it works




