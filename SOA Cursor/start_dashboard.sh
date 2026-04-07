#!/bin/bash
# Reliable Dashboard Startup Script

cd "/Users/kwhelan/pr-flow-ps/SOA Cursor"

echo "=================================================================================="
echo "STARTING SOA DASHBOARD"
echo "=================================================================================="
echo ""

# Kill any existing dashboard processes
echo "🔧 Clearing any existing processes..."
lsof -ti:5000 2>/dev/null | xargs kill -9 2>/dev/null
pkill -f "dashboard_enhanced.py" 2>/dev/null
pkill -f "dashboard.py" 2>/dev/null
sleep 1

# Check Flask
if ! python3 -c "import flask" 2>/dev/null; then
    echo "⚠️  Installing Flask..."
    pip3 install --break-system-packages flask 2>/dev/null || pip3 install --user flask 2>/dev/null
fi

# Check files
if [ ! -f "dashboard_enhanced.py" ]; then
    echo "❌ Error: dashboard_enhanced.py not found"
    exit 1
fi

if [ ! -f "soa_data_all_stis.csv" ]; then
    echo "⚠️  Warning: soa_data_all_stis.csv not found"
fi

echo "✅ Starting dashboard server..."
echo ""
echo "🌐 Dashboard will be available at: http://localhost:5000"
echo ""
echo "💡 IMPORTANT: Keep this terminal window open!"
echo "   The dashboard runs in this terminal"
echo "   Press Ctrl+C to stop"
echo ""
echo "💡 Browser will open automatically in 2 seconds"
echo ""
echo "=================================================================================="
echo ""

# Start dashboard in foreground so user can see it
# Browser will open automatically via Python script
python3 dashboard_enhanced.py
