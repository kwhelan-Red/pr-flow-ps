# How to Start the Dashboard

## Quick Start

**Open a NEW Terminal window** and run:

```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
./start_dashboard.sh
```

**Wait for this message:**
```
 * Running on http://0.0.0.0:5000
```

**Then open browser:**
```
http://localhost:5000
```

## Important Notes

1. **Keep the terminal window open** - Dashboard runs there
2. **Wait a few seconds** after starting before opening browser
3. **Don't close the terminal** - That stops the dashboard

## If "This site can't be reached"

### Check 1: Is Dashboard Running?

Look at the terminal - you should see:
```
 * Running on http://0.0.0.0:5000
```

If you don't see this:
- Check for error messages in terminal
- Make sure Flask is installed: `pip install --break-system-packages flask`

### Check 2: Try Different URL

- http://localhost:5000
- http://127.0.0.1:5000

### Check 3: Check Port

```bash
lsof -i:5000
```

Should show Python process listening on port 5000

### Check 4: Restart Dashboard

1. Press Ctrl+C in terminal (stops dashboard)
2. Run: `./start_dashboard.sh` again
3. Wait for "Running on..." message
4. Open browser

## Troubleshooting

**"Port 5000 already in use"**
```bash
lsof -ti:5000 | xargs kill -9
./start_dashboard.sh
```

**"Flask not found"**
```bash
pip install --break-system-packages flask
./start_dashboard.sh
```

**"File not found"**
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
pwd  # Should show: /Users/kwhelan/pr-flow-ps/SOA Cursor
./start_dashboard.sh
```

## Verify It's Working

Test with curl:
```bash
curl http://localhost:5000/api/status
```

If you see JSON, dashboard is working!

