#!/usr/bin/env python3
"""
Fixed Dashboard Startup Script
Checks dependencies and starts the dashboard
"""

import sys
import os
import subprocess

def check_and_install_flask():
    """Check if Flask is installed, install if not"""
    try:
        import flask
        print("✅ Flask is installed")
        return True
    except ImportError:
        print("⚠️  Flask not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ Flask installed successfully!")
            return True
        except Exception as e:
            print(f"❌ Error installing Flask: {e}")
            print("\n💡 Try manually: pip install flask")
            return False

def check_files():
    """Check if required files exist"""
    files_to_check = [
        ('dashboard.py', 'Dashboard server'),
        ('templates/dashboard.html', 'Dashboard HTML'),
        ('soa_data_all_stis.csv', 'CSV data file'),
        ('process_console_output.py', 'Processing script')
    ]
    
    all_exist = True
    for file_path, description in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {description}: {file_path}")
        else:
            print(f"❌ {description} NOT found: {file_path}")
            all_exist = False
    
    return all_exist

def main():
    print("="*80)
    print("SOA DASHBOARD STARTUP")
    print("="*80)
    print()
    
    # Check files
    if not check_files():
        print("\n⚠️  Some required files are missing!")
        print("   Make sure you're in the 'SOA Cursor' directory")
        return
    
    # Check Flask
    if not check_and_install_flask():
        return
    
    print("\n" + "="*80)
    print("STARTING DASHBOARD...")
    print("="*80)
    print("\n🌐 Dashboard will be available at: http://localhost:5000")
    print("💡 Press Ctrl+C to stop the server")
    print("="*80)
    print()
    
    # Import and run dashboard
    try:
        import dashboard
        dashboard.app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped")
    except Exception as e:
        print(f"\n❌ Error starting dashboard: {e}")
        print("\n💡 Try running directly: python3 dashboard.py")

if __name__ == '__main__':
    main()




