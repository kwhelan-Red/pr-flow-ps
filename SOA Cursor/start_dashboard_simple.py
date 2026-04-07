#!/usr/bin/env python3
"""
Simple Dashboard Starter - Shows exactly what's happening
"""

import sys
import os

print("="*80)
print("STARTING DASHBOARD - STEP BY STEP")
print("="*80)

# Check directory
print(f"\n1. Current directory: {os.getcwd()}")
if 'SOA Cursor' not in os.getcwd():
    print("   ⚠️  Wrong directory! Changing...")
    os.chdir('/Users/kwhelan/pr-flow-ps/SOA Cursor')
    print(f"   ✅ Now in: {os.getcwd()}")

# Check files
print("\n2. Checking files:")
files = ['dashboard_enhanced.py', 'soa_data_all_stis.csv', 'templates/dashboard_enhanced.html']
for f in files:
    if os.path.exists(f):
        print(f"   ✅ {f}")
    else:
        print(f"   ❌ {f} - MISSING!")

# Check Flask
print("\n3. Checking Flask:")
try:
    import flask
    print(f"   ✅ Flask installed")
except ImportError:
    print("   ❌ Flask NOT installed")
    print("   Installing...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "flask"])
    print("   ✅ Flask installed")

# Check port
print("\n4. Checking ports:")
import socket
for port in [5000, 5001]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    if result == 0:
        print(f"   ⚠️  Port {port} is in use")
    else:
        print(f"   ✅ Port {port} is available")

print("\n" + "="*80)
print("READY TO START")
print("="*80)
print("\n🚀 Starting dashboard now...")
print("   Keep this terminal window OPEN!")
print("   You'll see 'Running on...' message")
print("\n💡 After you see 'Running on...', open browser:")
print("   http://localhost:5000")
print("\n" + "="*80)
print()

# Import and run
try:
    from dashboard_enhanced import app
    import socket
    
    # Find available port
    port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    if result == 0:
        port = 5001
        print(f"⚠️  Port 5000 busy, using port {port}")
    
    print(f"\n🌐 Dashboard starting on port {port}...")
    print(f"📊 Open browser: http://localhost:{port}")
    print("\n💡 Press Ctrl+C to stop\n")
    
    # Auto-open browser
    import webbrowser
    import threading
    import time
    
    def open_browser_delayed():
        time.sleep(2)
        try:
            webbrowser.open(f"http://localhost:{port}")
        except:
            pass
    
    browser_thread = threading.Thread(target=open_browser_delayed, daemon=True)
    browser_thread.start()
    
    try:
        app.run(debug=True, host='127.0.0.1', port=port, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Error: Port {port} is already in use")
            print("   Solution: lsof -ti:{port} | xargs kill -9")
        else:
            raise
except KeyboardInterrupt:
    print("\n\n✅ Dashboard stopped")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()


