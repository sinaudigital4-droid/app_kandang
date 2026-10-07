"""
Client Python untuk memanggil Google Apps Script License Manager
Kompatibel dengan license_manager.py & Sistem Device Binding (1 Lisensi = 1 Perangkat)
"""

import requests
import urllib.parse
import uuid

SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyKsEzHJDEgnnFRFge-BroNnoPi858Gk95SlfoMJFytCKdxL1Y4_6DjAohmxgrh5-30/exec"

def get_device_hash():
    """Membuat atau mengambil ID perangkat unik untuk sesi browser pembeli ini."""
    try:
        import streamlit as st
        if 'device_uuid' not in st.session_state:
            st.session_state.device_uuid = str(uuid.uuid4())
        return st.session_state.device_uuid
    except Exception:
        # Fallback jika dijalankan di luar Streamlit
        return "default_device_client"

def check_license_google(license_key, device_hash=None):
    """Memeriksa lisensi sekaligus mengikatnya ke perangkat pembeli saat pertama kali digunakan."""
    if not device_hash:
        device_hash = get_device_hash()
        
    params = {
        'action': 'check',
        'key': license_key,
        'device_hash': device_hash
    }
    try:
        r = requests.get(SCRIPT_URL, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {'valid': False, 'message': f'Error koneksi: {str(e)}'}

def issue_license_google(user, expiry, features='all', device_hash='*'):
    """Membuat license key baru (secara default diset '*' agar siap dikunci ke perangkat pertama yang mengaktifkannya)."""
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

# Alias agar kompatibel dengan app.py
validate_license = check_license_google

if __name__ == '__main__':
    # Contoh testing lokal
    res_issue = issue_license_google('customer1', '2026-12-31', 'all', '*')
    print('Issue:', res_issue)
