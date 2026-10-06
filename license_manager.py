"""
Client Python untuk memanggil Google Apps Script License Manager
Kompatibel dengan license_manager.py
"""
import requests
import urllib.parse

SCRIPT_URL = "
https://script.google.com/macros/s/AKfycbyKsEzHJDEgnnFRFge-BroNnoPi858Gk95SlfoMJFytCKdxL1Y4_6DjAohmxgrh5-30/exec"

def check_license_google(license_key, device_hash=None):
    params = {
        'action': 'check',
        'key': license_key
    }
    if device_hash:
        params['device_hash'] = device_hash
    try:
        r = requests.get(SCRIPT_URL, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {'valid': False, 'message': f'Error koneksi: {str(e)}'}

def issue_license_google(user, expiry, features='all', device_hash='*'):
    params = {
        'action': 'issue',
        'user': user,
        'expiry': expiry,
        'features': features,
        'device_hash': device_hash
    }
    try:
        r = requests.get(SCRIPT_URL, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {'valid': False, 'message': f'Error koneksi: {str(e)}'}

if __name__ == '__main__':
    # Contoh issue lisensi baru otomatis dari Google Sheets
    res_issue = issue_license_google('customer1', '2026-12-31', 'all', '*')
    print('Issue:', res_issue)
    
    if res_issue.get('valid'):
        key = res_issue.get('key')
        # Contoh validasi balik
        res_check = check_license_google(key)
        print('Check:', res_check)
# Alias agar kompatibel dengan app.py
validate_license = check_license_google
