# PANDUAN SETUP & MENJALANKAN OTOMASI TEST
## Aplikasi DamnCRUD - Selenium + Python
---

## PRASYARAT

Pastikan sudah terinstall:
- ✅ Python 3.11 (sudah ada)
- ✅ Node.js 22 (sudah ada)
- ✅ PHP 8.2 (sudah ada)
- ⬜ XAMPP / Laragon (web server + MySQL)
- ⬜ Google Chrome (browser)

---

## LANGKAH 1: JALANKAN WEB SERVER & DATABASE

### 1A. Jika menggunakan XAMPP:
1. Buka XAMPP Control Panel
2. Klik **Start** pada **Apache**
3. Klik **Start** pada **MySQL**

### 1B. Import Database:
1. Buka browser → akses `http://localhost/phpmyadmin`
2. Klik **New** → buat database baru bernama **`badcrud`**
   - (Catatan: nama di functions.php adalah `badcrud`, bukan `damncrud`)
3. Pilih database `badcrud`
4. Klik tab **Import**
5. Pilih file: `DamnCRUD/db/damncrud.sql`
6. Klik **Go**
7. Sesuaikan data user: Pastikan tabel `users` berisi username `admin`

### 1C. Letakkan folder DamnCRUD di htdocs:
Copy folder `DamnCRUD` ke:
```
C:\xampp\htdocs\DamnCRUD\
```

### 1D. Verifikasi:
Buka browser → akses `http://localhost/DamnCRUD/login.php`
Harus muncul halaman login aplikasi.

---

## LANGKAH 2: INSTALL DEPENDENSI PYTHON

Buka **Command Prompt** atau **Terminal**, arahkan ke folder `automation`:
```
cd "e:\POLTEKSSN\TINGKAT 4\Pengujian Perangkat Lunak\UAS\automation"
```

Install semua library yang diperlukan:
```bash
pip install -r requirements.txt
```

Library yang akan diinstall:
- `selenium` - browser automation
- `webdriver-manager` - auto-download ChromeDriver
- `pytest` - test runner
- `pytest-html` - generate HTML report
- `pytest-ordering` - urutan eksekusi test

---

## LANGKAH 3: STRUKTUR FOLDER

Setelah setup, struktur folder akan seperti ini:
```
UAS/
├── automation/
│   ├── requirements.txt       ← daftar library Python
│   ├── conftest.py            ← konfigurasi global pytest
│   ├── config.py              ← konfigurasi URL & kredensial
│   ├── test_01_login.py       ← test autentikasi
│   ├── test_02_dashboard.py   ← test dashboard & session
│   ├── test_03_create.py      ← test tambah kontak
│   ├── test_04_update.py      ← test edit kontak
│   ├── test_05_delete.py      ← test hapus kontak
│   ├── test_06_profil.py      ← test upload foto
│   ├── test_07_logout.py      ← test logout
│   └── test_08_security.py    ← test keamanan
└── reports/                   ← hasil laporan HTML otomatis
```

---

## LANGKAH 4: JALANKAN TEST

### Jalankan SEMUA test sekaligus:
```bash
cd "e:\POLTEKSSN\TINGKAT 4\Pengujian Perangkat Lunak\UAS\automation"
pytest -v --html=../reports/hasil_pengujian.html --self-contained-html
```

### Jalankan test PER MODULE:
```bash
# Hanya test login
pytest test_01_login.py -v

# Hanya test CRUD
pytest test_03_create.py test_04_update.py test_05_delete.py -v

# Hanya test keamanan
pytest test_08_security.py -v
```

### Jalankan dengan output lebih detail:
```bash
pytest -v -s --tb=short
```

---

## LANGKAH 5: LIHAT LAPORAN

Setelah test selesai, buka file laporan HTML:
```
UAS/reports/hasil_pengujian.html
```
Buka dengan browser untuk melihat hasil lengkap dengan screenshot.

---

## TROUBLESHOOTING

| Masalah | Solusi |
|---|---|
| `ChromeDriver error` | Update Chrome ke versi terbaru, webdriver-manager akan auto-download driver |
| `Connection refused` | Pastikan XAMPP Apache & MySQL sudah Start |
| `Database error` | Import ulang SQL dan pastikan nama database `badcrud` |
| `ModuleNotFoundError` | Jalankan `pip install -r requirements.txt` ulang |
| `Timeout error` | Tambah waktu tunggu di `config.py`: ubah `TIMEOUT = 10` menjadi `20` |
