#!/usr/bin/env python3
"""
Smart Dashboard Launcher - Auto-detects and starts dashboard if needed
This prevents "127.0.0.1 refused to connect" errors
"""

import sys
import os
import socket
import time
import subprocess
import webbrowser
from pathlib import Path

def check_server_running(port=5000):
    """Check if dashboard server is running on given port"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False

def find_available_port(start_port=5000, max_port=5010):
    """Find an available port"""
    for port in range(start_port, max_port):
        if not check_server_running(port):
            return port
    return None

def check_flask_installed():
    """Check if Flask is installed"""
    try:
        import flask
        return True
    except ImportError:
        return False

def install_flask():
    """Install Flask if not available"""
    print("📦 Installing Flask...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "flask"], 
                      check=True, capture_output=True)
        return True
    except:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "flask"], 
                          check=True, capture_output=True)
            return True
        except:
            return False

def start_dashboard(port=5000):
    """Start the dashboard server"""
    # Change to correct directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check Flask
    if not check_flask_installed():
        if not install_flask():
            print("❌ Error: Could not install Flask")
            print("   Try manually: pip install flask")
            return False
    
    # Check if dashboard file exists
    dashboard_file = script_dir / "dashboard_enhanced.py"
    if not dashboard_file.exists():
        print(f"❌ Error: dashboard_enhanced.py not found in {script_dir}")
        return False
    
    print(f"🚀 Starting dashboard on port {port}...")
    print(f"📊 Dashboard will be available at: http://localhost:{port}")
    print("💡 Keep this terminal open! Press Ctrl+C to stop.\n")
    
    # Import and run dashboard
    try:
        sys.path.insert(0, str(script_dir))
        from dashboard_enhanced import app
        app.run(debug=True, host='127.0.0.1', port=port, use_reloader=False)
        return True
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped")
        return True
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        import traceback
        traceback.print_exc()
        return False

def open_browser(port=5000, delay=2):
    """Open browser after a delay"""
    time.sleep(delay)
    url = f"http://localhost:{port}"
    print(f"\n🌐 Opening browser: {url}")
    try:
        webbrowser.open(url)
    except:
        print(f"⚠️  Could not open browser automatically")
        print(f"   Please open manually: {url}")

def main():
    print("="*80)
    print("SOA DASHBOARD LAUNCHER")
    print("="*80)
    print()
    
    # Check if server is already running
    port = 5000
    if check_server_running(port):
        print(f"✅ Dashboard is already running on port {port}")
        print(f"📊 Open browser: http://localhost:{port}")
        open_browser(port, delay=0.5)
        return
    
    # Check port 5001
    if check_server_running(5001):
        print(f"✅ Dashboard is already running on port 5001")
        print(f"📊 Open browser: http://localhost:5001")
        open_browser(5001, delay=0.5)
        return
    
    # Find available port
    port = find_available_port()
    if port is None:
        print("❌ Error: No available ports (5000-5009)")
        print("   Please close other applications using these ports")
        return
    
    if port != 5000:
        print(f"⚠️  Port 5000 is in use, using port {port} instead")
    
    # Start dashboard
    print(f"\n🚀 Starting dashboard server...")
    start_dashboard(port)
    
    # Note: open_browser won't be called if server starts successfully
    # because app.run() blocks. We'll open browser in a separate thread
    # or the user can open it manually after seeing "Running on..."

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Launcher stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()



