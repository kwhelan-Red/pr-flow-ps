# SOA Data Extraction Dashboard

## Overview

A web-based dashboard for processing SOA data extraction from ServiceNow. Provides an easy-to-use interface for:
- Viewing extraction status
- Processing individual STI data
- Batch processing multiple STIs
- Exporting results

## Installation

### Prerequisites

```bash
pip install flask pandas
```

### Run the Dashboard

```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 dashboard.py
```

The dashboard will be available at: **http://localhost:5000**

## Features

### 1. Status Overview
- Real-time extraction progress
- Field completion statistics
- Visual progress bar

### 2. Process STI Data
- Select STI from dropdown
- Paste JSON from browser console
- Process and update CSV
- Load existing STI details

### 3. Batch Processing
- Process multiple STIs at once
- Paste batch JSON data
- View processing results

### 4. Export CSV
- Download current CSV file
- Get latest extraction results

## Usage

### Step 1: Start the Dashboard
```bash
python3 dashboard.py
```

### Step 2: Open Browser
Navigate to: http://localhost:5000

### Step 3: Process STI Data

1. **Get JSON from ServiceNow:**
   - Go to ServiceNow Business Application page
   - Press F12 (open console)
   - Click "Compliance" tab
   - Run JavaScript extraction script
   - Copy JSON output

2. **Process in Dashboard:**
   - Select STI from dropdown
   - Paste JSON into text area
   - Click "Process STI"
   - View success message

### Step 4: Check Status
- Status updates automatically
- View progress and field completion
- Export CSV when needed

## API Endpoints

- `GET /api/status` - Get extraction status
- `GET /api/stis` - Get list of all STIs
- `GET /api/stis/<sti>` - Get details for specific STI
- `POST /api/process` - Process JSON for an STI
- `POST /api/batch` - Process batch JSON data
- `GET /api/export` - Download CSV file

## Example API Usage

### Process Single STI
```bash
curl -X POST http://localhost:5000/api/process \
  -H "Content-Type: application/json" \
  -d '{
    "sti": "AAP-001",
    "json": "{\"applicationName\":\"App Name\",\"criticalityTier\":\"C1\",\"essUrl\":\"empty value\",\"piaUrl\":\"empty value\",\"dpqComplete\":\"empty value\"}"
  }'
```

### Get Status
```bash
curl http://localhost:5000/api/status
```

## Troubleshooting

**Dashboard won't start:**
- Check if Flask is installed: `pip install flask`
- Check if port 5000 is available
- Try a different port: Change `port=5000` in `dashboard.py`

**CSV file not found:**
- Make sure `soa_data_all_stis.csv` exists in the same directory
- Run `python3 helper.py` to verify CSV exists

**JSON processing errors:**
- Validate JSON format before processing
- Ensure JSON matches expected structure
- Check browser console for detailed errors

## Security Note

This dashboard runs on `localhost` by default. For production use:
- Add authentication
- Use HTTPS
- Restrict access to authorized users
- Validate all inputs server-side




