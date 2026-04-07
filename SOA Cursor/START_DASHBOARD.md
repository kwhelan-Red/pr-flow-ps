# How to Start the Dashboard

## Quick Start

```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 dashboard.py
```

Then open: **http://localhost:5000**

## If Flask is Not Installed

Install Flask first:

```bash
pip3 install --break-system-packages flask
```

Or try:

```bash
pip3 install --user flask
```

## Troubleshooting

**"Flask not found"**
- Run: `pip3 install --break-system-packages flask`

**"Port 5000 already in use"**
- Kill the process: `lsof -ti:5000 | xargs kill -9`

**"CSV file not found"**
- Make sure you're in the 'SOA Cursor' directory
- Check: `ls -la soa_data_all_stis.csv`

## Once Running

1. Open browser: http://localhost:5000
2. View extraction status
3. Process STI data by pasting JSON
4. Export CSV when done

