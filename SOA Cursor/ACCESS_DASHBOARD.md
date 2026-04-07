# How to Access the Dashboard

## ✅ Dashboard is Running!

The dashboard is currently running on port 5000.

## Open in Browser

Try these URLs:

1. **http://localhost:5000** (Recommended)
2. **http://127.0.0.1:5000**

## If "This site can't be reached"

### Check 1: Is Dashboard Running?

Look at your terminal - you should see:
```
 * Running on http://0.0.0.0:5000
```

If you don't see this, start the dashboard:
```bash
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
./start_dashboard.sh
```

### Check 2: Try Different Browser

- Chrome
- Firefox  
- Safari
- Edge

### Check 3: Clear Browser Cache

- Press Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
- Or try incognito/private mode

### Check 4: Check URL

Make sure you're using:
- ✅ http://localhost:5000
- ✅ http://127.0.0.1:5000
- ❌ NOT https://localhost:5000
- ❌ NOT http://localhost:5001

### Check 5: Restart Dashboard

```bash
# Stop current dashboard (Ctrl+C in terminal)
# Then restart:
cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"
lsof -ti:5000 | xargs kill -9
./start_dashboard.sh
```

## Verify Dashboard is Working

Test with curl:
```bash
curl http://localhost:5000/api/status
```

If you see JSON output, the dashboard is working!

## Still Not Working?

1. Check terminal for error messages
2. Make sure you're using http:// (not https://)
3. Try a different port (edit dashboard_enhanced.py, change port=5000 to port=5001)
4. Check if antivirus/firewall is blocking localhost

