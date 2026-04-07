# Permanent Fix for "127.0.0.1 refused to connect" Error

## Problem
When trying to access the dashboard at `http://localhost:5000` or `http://127.0.0.1:5000`, you get:
```
This site can't be reached
127.0.0.1 refused to connect.
```

This happens because **the dashboard server isn't running**.

## Permanent Solution

### Option 1: Use the Smart Launcher (RECOMMENDED)

A new smart launcher has been created that automatically:
- ✅ Checks if dashboard is already running
- ✅ Starts it if not running
- ✅ Opens browser automatically
- ✅ Handles port conflicts
- ✅ Installs Flask if needed

**To use:**
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 launch_dashboard.py
```

This will:
1. Check if dashboard is running (ports 5000 or 5001)
2. If running, open browser automatically
3. If not running, start it and open browser
4. Handle all errors gracefully

### Option 2: Use the Shell Script

```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
./start_dashboard.sh
```

### Option 3: Direct Python Script

```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 dashboard_enhanced.py
```

## What Was Fixed

### 1. Auto-Browser Opening
- Dashboard now automatically opens your browser after starting
- No more manual URL typing needed

### 2. Better Error Messages
- Clear messages when port is in use
- Instructions on how to fix port conflicts

### 3. Smart Port Detection
- Automatically finds available port (5000 or 5001)
- Handles port conflicts gracefully

### 4. Server Status Checking
- New launcher checks if server is already running
- Prevents duplicate servers

## Quick Reference

### Start Dashboard
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
python3 launch_dashboard.py
```

### Check if Dashboard is Running
```bash
curl http://localhost:5000/api/status
```

### Stop Dashboard
Press `Ctrl+C` in the terminal where it's running

### Kill Stuck Process
```bash
lsof -ti:5000 | xargs kill -9
```

## Troubleshooting

### "Port already in use"
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use port 5001
python3 dashboard_enhanced.py
# (It will auto-detect and use 5001)
```

### "Flask not found"
```bash
pip install --break-system-packages flask
```

### "Dashboard file not found"
```bash
# Make sure you're in the right directory
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
ls -la dashboard_enhanced.py
```

## How It Works Now

1. **Run launcher**: `python3 launch_dashboard.py`
2. **Launcher checks**: Is dashboard running?
3. **If yes**: Opens browser automatically
4. **If no**: Starts dashboard, then opens browser
5. **Browser opens**: Automatically after 2 seconds
6. **Dashboard ready**: Use it normally

## Prevention

The error is now prevented because:
- ✅ Launcher checks server status before trying to connect
- ✅ Dashboard auto-opens browser so you know it's running
- ✅ Better error messages guide you if something goes wrong
- ✅ Port conflicts are handled automatically

## Files Updated

- ✅ `dashboard_enhanced.py` - Auto-opens browser, better error handling
- ✅ `start_dashboard_simple.py` - Auto-opens browser
- ✅ `launch_dashboard.py` - NEW smart launcher
- ✅ `start_dashboard.sh` - Updated instructions

You should **never see the "refused to connect" error again** if you use the launcher!



