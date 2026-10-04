"""
License Manager Hybrid - Offline HMAC + Expiry + Device binding
Simple dan mudah dipakai user, cukup aman untuk penjualan digital.

CARA MENGGUNAKAN:
1. GANTI SECRET_KEY di bawah ini dengan key rahasia Anda sendiri, jangan dibagikan
2. Buat license key dengan fungsi generate_license() atau via script terpisah
3. User paste license key di sidebar app

Format license key: BASE64(payload).signature
payload = user|expiry_date(YYYY-MM-DD)|features|device_hash
signature = HMAC-SHA256(payload, SECRET_KEY)
"""

import hashlib
import hmac
import base64
from datetime import datetime, date
import platform
import uuid

# ==================== KONFIGURASI - GANTI INI ====================
# !!! GANTI SECRET_KEY INI DENGAN KEY RAHASIA ANDA SENDIRI !!!
# Contoh dummy, jangan dipakai untuk produksi
SECRET_KEY = b"YOUR_SECRET_KEY_CHANGE_ME_1234567890ABCDEF"

# ==================== UTILITAS ====================

def get_device_hash():
    # Binding ringan ke device, membuat license tidak mudah dipindah-pindah
    node = uuid.getnode()
    machine = platform.node()
    raw = f"{node}-{machine}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

DEVICE_HASH = get_device_hash()

def encode_payload(payload_str: str) -> str:
    return base64.urlsafe_b64encode(payload_str.encode()).decode().rstrip("=")

def decode_payload(payload_b64: str) -> str:
    # Pad base64
    padding = "=" * (-len(payload_b64) % 4)
    decoded = base64.urlsafe_b64decode(payload_b64 + padding)
    return decoded.decode()

def make_signature(payload_str: str) -> str:
    sig = hmac.new(SECRET_KEY, payload_str.encode(), hashlib.sha256).hexdigest()
    return sig

# ==================== GENERATE LICENSE - UNTUK ANDA SEBAGAI PENJUAL ====================
def generate_license(user: str, expiry_date: str, features: str = "all", device_hash: str = None):
    """
    Gunakan fungsi ini untuk membuat license key baru.
    Contoh:
        key = generate_license("customer1", "2027-12-31")
    """
    if device_hash is None:
        device_hash = "*"  # * = bebas device, atau isi dengan hash spesifik customer
    payload = f"{user}|{expiry_date}|{features}|{device_hash}"
    sig = make_signature(payload)
    license_key = f"{encode_payload(payload)}.{sig}"
    return license_key

# ==================== VALIDASI LICENSE - DIPAKAI DI APP ====================
def validate_license(license_key: str):
    """
    Mengembalikan dict: {valid: bool, message: str, user: str, expiry: date, features: str}
    """
    try:
        if not license_key or "." not in license_key:
            return {"valid": False, "message": "Format license tidak valid"}

        payload_b64, sig = license_key.rsplit(".", 1)
        payload = decode_payload(payload_b64)

        # Verifikasi signature
        expected_sig = make_signature(payload)
        if not hmac.compare_digest(expected_sig, sig):
            return {"valid": False, "message": "Signature tidak cocok, license palsu"}

        parts = payload.split("|")
        if len(parts) != 4:
            return {"valid": False, "message": "Payload rusak"}

        user, expiry_str, features, license_device = parts

        # Cek expiry
        try:
            expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        except ValueError:
            return {"valid": False, "message": "Format tanggal expiry salah"}

        today = date.today()
        if today > expiry_date:
            return {"valid": False, "message": f"Lisensi kedaluwarsa pada {expiry_date}"}

        # Cek device binding
        if license_device != "*" and license_device != DEVICE_HASH:
            return {"valid": False, "message": "Lisensi tidak cocok untuk perangkat ini"}

        return {
            "valid": True,
            "message": "Lisensi valid",
            "user": user,
            "expiry": expiry_date,
            "features": features
        }
    except Exception as e:
        return {"valid": False, "message": f"Error validasi: {str(e)}"}

# Contoh penggunaan generate saat testing
if __name__ == "__main__":
    # GANTI INI saat membuat license untuk customer
    demo_key = generate_license("demo_user", "2027-12-31", "all", "*")
    print("Contoh License Key:")
    print(demo_key)
    print("\nValidasi:")
    print(validate_license(demo_key))
