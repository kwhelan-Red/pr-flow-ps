# How to Process All STIs

## Overview

To process all 114 STIs, you need JSON data for each one. Here are your options:

## Option 1: Batch Process from Single JSON File

**Step 1:** Create a JSON file with all STI data:
```json
{
  "AAP-001": {
    "applicationName": "AAP Application",
    "criticalityTier": "C1",
    "essUrl": "empty value",
    "piaUrl": "empty value",
    "dpqComplete": "empty value"
  },
  "ANSI-001": {
    "applicationName": "ANSI Application",
    "criticalityTier": "C2",
    "essUrl": "empty value",
    "piaUrl": "empty value",
    "dpqComplete": "empty value"
  }
  // ... add all 114 STIs
}
```

**Step 2:** Process the file:
```bash
python3 batch_process_all.py --file all_stis_data.json
```

## Option 2: Batch Process from Directory (One File Per STI)

**Step 1:** Create directory and save JSON files:
```bash
mkdir -p console_outputs
# Save each STI's JSON as: console_outputs/AAP-001.json, console_outputs/ANSI-001.json, etc.
```

**Step 2:** Process all files:
```bash
python3 batch_process_all.py --dir console_outputs/
```

## Option 3: Create Template and Fill In

**Step 1:** Generate template:
```bash
python3 batch_process_all.py --template
```

**Step 2:** Edit `batch_template.json` with your data

**Step 3:** Process:
```bash
python3 batch_process_all.py --file batch_template.json
```

## Option 4: Manual Processing (One at a Time)

For each STI:
```bash
python3 process_console_output.py --sti <STI> --json '<JSON>'
```

## Getting JSON Data

To get JSON data for each STI:

1. Navigate to ServiceNow page for the STI
2. Press F12 (open console)
3. Click "Compliance" tab
4. Run JavaScript extraction script (see QUICK_START.md)
5. Copy JSON output
6. Save to file or add to batch JSON

## Current Status

Check progress anytime:
```bash
python3 check_extraction_status.py
```

## Example: Process Sample Batch

I've created a sample batch file with 3 STIs:
```bash
python3 batch_process_all.py --file sample_batch.json
```

This demonstrates how batch processing works!




