# config.py - Konfigurasi Global untuk Test Otomasi DamnCRUD

# URL Aplikasi (sesuaikan jika port atau path berbeda)
BASE_URL = "http://localhost:8080/DamnCRUD"

# Kredensial Login Valid
VALID_USERNAME = "admin"
VALID_PASSWORD = "nimda666!"

# Kredensial Login Tidak Valid
INVALID_USERNAME = "userpalsu"
INVALID_PASSWORD = "passwordsalah"

# Timeout (detik) untuk menunggu elemen muncul
TIMEOUT = 10

# Data kontak untuk pengujian tambah kontak
TEST_CONTACT = {
    "name":  "Test Otomasi",
    "email": "test.otomasi@email.com",
    "phone": "081234567890",
    "title": "QA Engineer"
}

# Data update kontak
UPDATE_CONTACT = {
    "name":  "Test Otomasi Updated",
    "email": "updated.otomasi@email.com",
    "phone": "089876543210",
    "title": "Senior QA"
}
