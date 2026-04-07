# Start Dashboard Now

## Quick Start (Copy and Paste)

```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
./start_dashboard.sh
```

Then open: **http://localhost:5000**

## If That Doesn't Work

```bash
# 1. Go to directory
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"

# 2. Install Flask (if needed)
pip install --break-system-packages flask

# 3. Clear port 5000
lsof -ti:5000 | xargs kill -9

# 4. Start dashboard
python3 dashboard_enhanced.py
```

## What You Should See

In the terminal:
```
🌐 Starting web server...
📊 Dashboard will be available at: http://localhost:5000
 * Running on http://0.0.0.0:5000
```

Then open browser: http://localhost:5000

