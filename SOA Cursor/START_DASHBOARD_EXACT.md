# EXACT Steps to Start Dashboard

## Step-by-Step (Copy and Paste)

### 1. Open Terminal
- Press `Cmd + Space`
- Type: `Terminal`
- Press Enter

### 2. Copy These Commands (One at a Time)

```bash
cd '/Users/kwhelan/pr-flow-ps/SOA Cursor'
```

Press Enter, then:

```bash
python3 start_dashboard_simple.py
```

### 3. Wait for This Message

You should see:
```
🌐 Dashboard starting on port 5000...
📊 Open browser: http://localhost:5000
 * Running on http://127.0.0.1:5000
```

### 4. Keep Terminal Open

**IMPORTANT:** Don't close the terminal window!
The dashboard runs in that terminal.

### 5. Open Browser

Once you see "Running on...", open:
- http://localhost:5000
- OR http://127.0.0.1:5000

## If Still Not Working

### Check 1: Is Dashboard Running?

Look at terminal - do you see:
```
 * Running on http://127.0.0.1:5000
```

If NO:
- Check for error messages in terminal
- Make sure Flask is installed: `pip install --break-system-packages flask`

### Check 2: Try Different URL

- http://localhost:5000
- http://127.0.0.1:5000
- http://localhost:5001
- http://127.0.0.1:5001

### Check 3: Wait Longer

Sometimes it takes 5-10 seconds to start.
Wait for "Running on..." message before opening browser.

### Check 4: Check Port

```bash
lsof -i:5000
```

Should show Python process.

## Still Not Working?

Run this to see what's happening:
```bash
cd '/Users/kwhelan/pr-flow-ps/SOA Cursor'
python3 start_dashboard_simple.py
```

Watch the output - it will tell you what's wrong!

