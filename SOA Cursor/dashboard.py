#!/usr/bin/env python3
"""
SOA Data Extraction Dashboard
Web interface for running scripts and viewing results
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import json
import os
from datetime import datetime
from process_console_output import parse_console_output, update_csv_with_results

app = Flask(__name__)

CSV_FILE = 'soa_data_all_stis.csv'

def get_status():
    """Get current extraction status"""
    try:
        df = pd.read_csv(CSV_FILE)
        total = len(df)
        extracted = len(df[df['Status'].str.contains('Extracted', na=False)])
        pending = total - extracted
        
        # Field completion
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
            'fields': fields
        }
    except Exception as e:
        return {'error': str(e)}

def get_stis():
    """Get list of all STIs"""
    try:
        df = pd.read_csv(CSV_FILE)
        return df['STI'].tolist()
    except:
        return []

@app.route('/')
def index():
    """Main dashboard page"""
    status = get_status()
    stis = get_stis()
    # Try enhanced dashboard first, fallback to regular
    if os.path.exists('templates/dashboard_enhanced.html'):
        return render_template('dashboard_enhanced.html', status=status, stis=stis)
    return render_template('dashboard.html', status=status, stis=stis)

@app.route('/api/status')
def api_status():
    """API endpoint for status"""
    return jsonify(get_status())

@app.route('/api/stis')
def api_stis():
    """API endpoint for STI list"""
    return jsonify(get_stis())

@app.route('/api/process', methods=['POST'])
def api_process():
    """Process JSON data for an STI"""
    try:
        data = request.json
        sti = data.get('sti')
        json_data = data.get('json')
        
        if not sti or not json_data:
            return jsonify({'error': 'Missing STI or JSON data'}), 400
        
        # Parse JSON
        if isinstance(json_data, str):
            results = parse_console_output(json_data)
        else:
            results = json_data
        
        if not results:
            return jsonify({'error': 'Could not parse JSON'}), 400
        
        # Update CSV
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

@app.route('/api/stis/<sti>')
def api_sti_details(sti):
    """Get details for a specific STI"""
    try:
        df = pd.read_csv(CSV_FILE)
        sti_data = df[df['STI'] == sti]
        
        if sti_data.empty:
            return jsonify({'error': 'STI not found'}), 404
        
        row = sti_data.iloc[0]
        return jsonify({
            'sti': sti,
            'applicationName': row.get('Application Name', ''),
            'criticalityTier': row.get('Criticality Tier', ''),
            'essUrl': row.get('ESS Assessment URL', ''),
            'piaUrl': row.get('PIA Assessment URL', ''),
            'dpqComplete': row.get('DPQ Complete', ''),
            'status': row.get('Status', ''),
            'collectionDate': row.get('Collection Date', '')
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

if __name__ == '__main__':
    print("="*80)
    print("SOA DATA EXTRACTION DASHBOARD")
    print("="*80)
    print("\n🌐 Starting web server...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*80)
    # Try port 5000, fallback to 5001 if in use
    import socket
    port = 5000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    if result == 0:
        print(f"⚠️  Port {port} is in use, trying port 5001...")
        port = 5001
    
    print(f"\n🌐 Dashboard available at: http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)

