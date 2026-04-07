# Dashboard Troubleshooting Guide

## "This site can't be reached" Error

This means the dashboard server isn't running. Here's how to fix it:

### Step 1: Check if Dashboard is Running

```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
ps aux | grep dashboard
```

If you see a process, the dashboard is running. If not, continue to Step 2.

### Step 2: Start the Dashboard

**Easiest way:**
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
./start_dashboard.sh
```

**Or manually:**
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 dashboard_enhanced.py
```

### Step 3: Check for Errors

Look at the terminal output. Common issues:

**"Flask not found"**
```bash
pip install --break-system-packages flask
```

**"Port 5000 already in use"**
```bash
lsof -ti:5000 | xargs kill -9
python3 dashboard_enhanced.py
```

**"CSV file not found"**
```bash
# Make sure you're in the right directory
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
ls -la soa_data_all_stis.csv
```

### Step 4: Verify Dashboard is Running

**Check terminal output:**
You should see:
```
🌐 Starting web server...
📊 Dashboard will be available at: http://localhost:5000
 * Running on http://0.0.0.0:5000
```

**Test in browser:**
Open: http://localhost:5000

**Test with curl:**
```bash
curl http://localhost:5000/api/status
```

### Step 5: If Still Not Working

**Try a different port:**

Edit `dashboard_enhanced.py` and change:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```
to:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

Then access: http://localhost:5001

**Check firewall:**
Make sure your firewall isn't blocking port 5000.

**Check if Python is working:**
```bash
python3 --version
python3 -c "import flask; print('Flask OK')"
```

## Quick Fix Commands

```bash
# Kill any process on port 5000
lsof -ti:5000 | xargs kill -9

# Install Flask
pip install --break-system-packages flask

# Start dashboard
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 dashboard_enhanced.py
```

## Still Having Issues?

1. Check terminal for error messages
2. Make sure you're in the right directory
3. Verify Flask is installed: `python3 -c "import flask"`
4. Try the regular dashboard: `python3 dashboard.py`
5. Check if port 5000 is available: `lsof -i:5000`




