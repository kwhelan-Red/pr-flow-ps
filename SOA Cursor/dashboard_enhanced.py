#!/usr/bin/env python3
"""
Enhanced Dashboard with Automated Extraction
Adds background job processing and real-time updates
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import json
import os
import threading
import time
from datetime import datetime
from process_console_output import parse_console_output, update_csv_with_results

app = Flask(__name__)

CSV_FILE = 'soa_data_all_stis.csv'
PROGRESS_FILE = 'extraction_progress.json'

# Global extraction status
extraction_status = {
    'running': False,
    'current_sti': None,
    'processed': 0,
    'failed': 0,
    'total': 0,
    'start_time': None
}

def get_status():
    """Get current extraction status"""
    try:
        df = pd.read_csv(CSV_FILE)
        total = len(df)
        extracted = len(df[df['Status'].str.contains('Extracted', na=False)])
        pending = total - extracted
        
        fields = {
            'Application Name': len(df[df['Application Name'].notna() & (df['Application Name'] != 'empty value') & (df['Application Name'] != '')]),
            'Criticality Tier': len(df[df['Criticality Tier'].notna() & (df['Criticality Tier'] != 'empty value') & (df['Criticality Tier'] != '')]),
            'ESS Assessment URL': len(df[df['ESS Assessment URL'].notna() & (df['ESS Assessment URL'] != 'empty value') & (df['ESS Assessment URL'] != '')]),
            'PIA Assessment URL': len(df[df['PIA Assessment URL'].notna() & (df['PIA Assessment URL'] != 'empty value') & (df['PIA Assessment URL'] != '')]),
            'DPQ Complete': len(df[df['DPQ Complete'].notna() & (df['DPQ Complete'] != 'empty value') & (df['DPQ Complete'] != '')])
        }
        
        return {
            'total': total,
            'extracted': extracted,
            'pending': pending,
            'fields': fields,
            'extraction': extraction_status
        }
    except Exception as e:
        return {'error': str(e)}

def run_automated_extraction(method='playwright', start_from=0, max_stis=None):
    """Run automated extraction in background"""
    global extraction_status
    
    extraction_status['running'] = True
    extraction_status['start_time'] = datetime.now().isoformat()
    
    try:
        # Import and run extraction
        import subprocess
        import sys
        
        cmd = [sys.executable, 'extract_all_automated.py', '--method', method]
        if start_from > 0:
            cmd.extend(['--start-from', str(start_from)])
        if max_stis:
            cmd.extend(['--max', str(max_stis)])
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Monitor progress
        for line in process.stdout:
            if 'Processing' in line:
                # Extract STI name from log
                parts = line.split()
                for part in parts:
                    if '-' in part and part[0].isalpha():
                        extraction_status['current_sti'] = part
                        extraction_status['processed'] += 1
                        break
            if 'Failed' in line or 'Error' in line:
                extraction_status['failed'] += 1
        
        process.wait()
        
    except Exception as e:
        print(f"Error in extraction: {e}")
    finally:
        extraction_status['running'] = False
        extraction_status['current_sti'] = None

@app.route('/')
def index():
    """Main dashboard page"""
    status = get_status()
    stis = []
    try:
        df = pd.read_csv(CSV_FILE)
        stis = df['STI'].tolist()
    except:
        pass
    return render_template('dashboard_enhanced.html', status=status, stis=stis)

@app.route('/api/status')
def api_status():
    """API endpoint for status"""
    return jsonify(get_status())

@app.route('/api/stis')
def api_stis():
    """API endpoint for STI list"""
    try:
        df = pd.read_csv(CSV_FILE)
        return jsonify(df['STI'].tolist())
    except:
        return jsonify([])

@app.route('/api/process', methods=['POST'])
def api_process():
    """Process JSON data for an STI"""
    try:
        data = request.json
        sti = data.get('sti')
        json_data = data.get('json')
        
        if not sti or not json_data:
            return jsonify({'error': 'Missing STI or JSON data'}), 400
        
        if isinstance(json_data, str):
            results = parse_console_output(json_data)
        else:
            results = json_data
        
        if not results:
            return jsonify({'error': 'Could not parse JSON'}), 400
        
        success = update_csv_with_results(CSV_FILE, sti, results)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Updated {sti}',
                'results': results
            })
        else:
            return jsonify({'error': f'STI {sti} not found in CSV'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extract/start', methods=['POST'])
def api_extract_start():
    """Start automated extraction"""
    global extraction_status
    
    if extraction_status['running']:
        return jsonify({'error': 'Extraction already running'}), 400
    
    data = request.json or {}
    method = data.get('method', 'playwright')
    start_from = data.get('start_from', 0)
    max_stis = data.get('max_stis')
    
    # Reset status
    extraction_status = {
        'running': True,
        'current_sti': None,
        'processed': 0,
        'failed': 0,
        'total': len(load_stis()),
        'start_time': datetime.now().isoformat()
    }
    
    # Start extraction in background thread
    thread = threading.Thread(
        target=run_automated_extraction,
        args=(method, start_from, max_stis)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Extraction started',
        'status': extraction_status
    })

@app.route('/api/extract/stop', methods=['POST'])
def api_extract_stop():
    """Stop automated extraction"""
    global extraction_status
    extraction_status['running'] = False
    return jsonify({'success': True, 'message': 'Extraction stopped'})

@app.route('/api/extract/status', methods=['GET'])
def api_extract_status():
    """Get extraction status"""
    return jsonify(extraction_status)

@app.route('/api/batch', methods=['POST'])
def api_batch():
    """Process batch JSON data"""
    try:
        data = request.json
        batch_data = data.get('batch', {})
        
        results = []
        errors = []
        
        for sti, json_data in batch_data.items():
            try:
                if isinstance(json_data, str):
                    parsed = parse_console_output(json_data)
                else:
                    parsed = json_data
                
                if parsed:
                    success = update_csv_with_results(CSV_FILE, sti, parsed)
                    if success:
                        results.append(sti)
                    else:
                        errors.append(f'{sti}: Not found in CSV')
                else:
                    errors.append(f'{sti}: Could not parse JSON')
            except Exception as e:
                errors.append(f'{sti}: {str(e)}')
        
        return jsonify({
            'success': True,
            'processed': len(results),
            'results': results,
            'errors': errors
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data')
def api_data():
    """Get extracted data as JSON"""
    try:
        df = pd.read_csv(CSV_FILE)
        # Convert DataFrame to JSON, handling NaN values
        df = df.fillna('')
        # Convert to records format for easier frontend handling
        records = df.to_dict('records')
        return jsonify({
            'success': True,
            'data': records,
            'columns': list(df.columns)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export')
def api_export():
    """Export CSV file"""
    try:
        return send_file(CSV_FILE, as_attachment=True, download_name='soa_data_all_stis.csv')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def load_stis():
    """Load STI list"""
    try:
        df = pd.read_csv(CSV_FILE)
        return df['STI'].tolist()
    except:
        return []

if __name__ == '__main__':
    print("="*80)
    print("SOA DATA EXTRACTION DASHBOARD - ENHANCED")
    print("="*80)
    print("\n🌐 Starting web server...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("\n💡 Features:")
    print("   ✅ Manual STI processing")
    print("   ✅ Automated extraction for all STIs")
    print("   ✅ Real-time progress tracking")
    print("   ✅ Batch processing")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*80)
    # Try port 5000, fallback to 5001 if in use
    import socket
    import webbrowser
    import threading
    
    port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    if result == 0:
        print(f"⚠️  Port {port} is in use, trying port 5001...")
        port = 5001
    
    url = f"http://localhost:{port}"
    print(f"\n🌐 Dashboard available at: {url}")
    
    # Auto-open browser after a short delay
    def open_browser_delayed():
        time.sleep(2)  # Wait for server to start
        try:
            webbrowser.open(url)
            print(f"✅ Browser opened automatically")
        except:
            print(f"⚠️  Could not open browser automatically")
            print(f"   Please open manually: {url}")
    
    browser_thread = threading.Thread(target=open_browser_delayed, daemon=True)
    browser_thread.start()
    
    try:
        app.run(debug=True, host='127.0.0.1', port=port, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Error: Port {port} is already in use")
            print("   Try:")
            print(f"   1. Kill process on port {port}: lsof -ti:{port} | xargs kill -9")
            print(f"   2. Or use a different port")
        else:
            raise

