# DOKUMEN TEST PLAN
## Pengujian Aplikasi DamnCRUD
### Ujian Akhir Semester - Pengujian Perangkat Lunak

---

| Informasi Dokumen | Detail |
|---|---|
| Nama Dokumen | Test Plan Aplikasi DamnCRUD |
| Versi | 1.0 |
| Tanggal | 23 Februari 2026 |
| Mata Kuliah | Pengujian Perangkat Lunak |
| Program Studi | Politeknik SSN |

---

## 1. PENDAHULUAN

### 1.1 Tujuan
Dokumen ini mendeskripsikan rencana pengujian (test plan) terhadap aplikasi web **DamnCRUD** yang merupakan aplikasi CRUD berbasis PHP untuk pengelolaan data kontak. Pengujian mencakup aspek fungsional dan keamanan (security) dari aplikasi.

### 1.2 Ruang Lingkup (Scope)
Pengujian dilakukan terhadap seluruh modul aplikasi DamnCRUD, meliputi:
- Modul Autentikasi (Login & Logout)
- Modul Dashboard (Tampilan Daftar Kontak)
- Modul Tambah Kontak (Create)
- Modul Edit Kontak (Update)
- Modul Hapus Kontak (Delete)
- Modul Profil (Upload Foto)
- Modul Halaman Uji XSS (vpage.php)

### 1.3 Referensi
- Source code aplikasi DamnCRUD (PHP)
- Database schema: `db/damncrud.sql`
- OWASP Top 10 Web Application Security Risks
- IEEE 829 Standard for Software Test Documentation

---

## 2. GAMBARAN SISTEM YANG DIUJI

### 2.1 Deskripsi Aplikasi
DamnCRUD adalah aplikasi web berbasis PHP yang memungkinkan pengguna untuk mengelola data kontak (nama, email, telepon, jabatan). Aplikasi ini dirancang sebagai sarana pembelajaran pengujian keamanan web.

### 2.2 Arsitektur Sistem

```
┌─────────────┐      ┌─────────────┐      ┌──────────────┐
│   Browser   │ ───► │  PHP (Web)  │ ───► │  MySQL (DB)  │
│  (Client)   │ ◄─── │  localhost  │ ◄─── │  badcrud     │
└─────────────┘      └─────────────┘      └──────────────┘
```

### 2.3 Teknologi
| Komponen | Teknologi |
|---|---|
| Backend | PHP |
| Frontend | HTML5, Bootstrap 4.6.0 |
| Database | MySQL / MariaDB |
| Library JS | jQuery 3.5.1, DataTables 1.10.20 |

### 2.4 Struktur File Aplikasi
| File | Fungsi |
|---|---|
| `login.php` | Halaman autentikasi pengguna |
| `index.php` | Dashboard & daftar kontak |
| `create.php` | Form tambah kontak baru |
| `update.php` | Form edit kontak |
| `delete.php` | Proses hapus kontak |
| `profil.php` | Halaman profil & upload foto |
| `logout.php` | Proses keluar sesi |
| `vpage.php` | Halaman dummy untuk uji XSS |
| `functions.php` | Fungsi koneksi database & helper |
| `menu.php` | Komponen navigasi |

---

## 3. TUJUAN PENGUJIAN

### 3.1 Tujuan Fungsional
- Memverifikasi bahwa setiap fitur bekerja sesuai spesifikasi
- Memastikan alur kerja (workflow) aplikasi berjalan dengan benar
- Mengidentifikasi bug dan error pada fitur-fitur utama

### 3.2 Tujuan Keamanan
- Mengidentifikasi celah SQL Injection pada form login
- Mengidentifikasi celah Cross-Site Scripting (XSS) pada vpage.php
- Mengidentifikasi kelemahan validasi upload file pada profil.php
- Mengidentifikasi masalah manajemen sesi (session management)
- Mengidentifikasi hardcoded credentials pada source code

---

## 4. STRATEGI PENGUJIAN

### 4.1 Jenis Pengujian
| Jenis Pengujian | Metode | Keterangan |
|---|---|---|
| **Functional Testing** | Black-box | Menguji fitur berdasarkan input/output |
| **Security Testing** | Black-box + Code Review | Menguji celah keamanan |
| **Negative Testing** | Black-box | Menguji dengan input tidak valid |
| **Boundary Testing** | Black-box | Menguji batas nilai input |
| **Session Testing** | Black-box | Menguji manajemen sesi |

### 4.2 Teknik Pengujian
- **Equivalence Partitioning**: Membagi input ke dalam kelompok valid dan tidak valid
- **Boundary Value Analysis**: Menguji nilai batas input
- **Error Guessing**: Menebak kemungkinan error berdasarkan pengalaman
- **Code Review (Static Analysis)**: Analisis kode sumber untuk menemukan celah keamanan

### 4.3 Tingkat Keparahan Bug
| Level | Deskripsi | Contoh |
|---|---|---|
| **Critical** | Sistem tidak dapat berfungsi / celah keamanan kritis | SQL Injection, data corruption |
| **High** | Fitur utama tidak berfungsi / celah keamanan tinggi | XSS, session tidak aman |
| **Medium** | Fitur tidak berfungsi sebagian / bug signifikan | Field tidak terisi, validasi salah |
| **Low** | Masalah minor yang tidak mempengaruhi fungsi utama | Typo, tampilan kecil |

---

## 5. LINGKUNGAN PENGUJIAN (TEST ENVIRONMENT)

### 5.1 Konfigurasi Sistem
| Item | Spesifikasi |
|---|---|
| Operating System | Windows |
| Web Server | Apache (XAMPP/WAMP/Laragon) |
| PHP Version | PHP 7.x / 8.x |
| Database | MySQL / MariaDB |
| Browser | Google Chrome / Mozilla Firefox |
| Tools Pengujian | Browser DevTools, Burp Suite (opsional) |

### 5.2 Konfigurasi Database
| Parameter | Nilai |
|---|---|
| Host | localhost |
| Database | badcrud |
| Username | root |
| Password | root123 |

### 5.3 Kredensial Uji
| Parameter | Nilai |
|---|---|
| Username (valid) | admin |
| Password (valid) | nimda666! |
| URL Aplikasi | http://localhost/DamnCRUD/ |

---

## 6. KRITERIA PENGUJIAN

### 6.1 Kriteria Mulai Pengujian (Entry Criteria)
- Aplikasi sudah berhasil diinstall dan dapat diakses melalui browser
- Database sudah diimport dan berisi data awal
- Semua file konfigurasi sudah benar

### 6.2 Kriteria Selesai Pengujian (Exit Criteria)
- Seluruh test case sudah dieksekusi
- Semua bug critical dan high sudah dilaporkan
- Laporan pengujian sudah dibuat

### 6.3 Kriteria Suspensi (Suspension Criteria)
- Aplikasi tidak dapat diakses (server down)
- Database tidak dapat terhubung
- Error fatal yang mencegah pengujian berlanjut

---

## 7. RISIKO PENGUJIAN

| Risiko | Kemungkinan | Dampak | Mitigasi |
|---|---|---|---|
| Server tidak tersedia | Rendah | Tinggi | Pastikan XAMPP/WAMP berjalan |
| Database error | Rendah | Tinggi | Import ulang damncrud.sql |
| Data uji terhapus | Sedang | Sedang | Backup database sebelum pengujian |
| Browser incompatibility | Rendah | Rendah | Gunakan Chrome versi terbaru |

---

## 8. DELIVERABLES (OUTPUT PENGUJIAN)

1. **Test Plan** (dokumen ini)
2. **Test Cases** - Daftar kasus uji lengkap
3. **Laporan Hasil Pengujian** - Hasil eksekusi test case dan temuan bug
4. **Bug Report** - Laporan detail setiap bug yang ditemukan

---

## 9. JADWAL PENGUJIAN

| Aktivitas | Keterangan |
|---|---|
| Persiapan & Instalasi | Setup environment pengujian |
| Pembuatan Test Case | Penulisan semua kasus uji |
| Eksekusi Pengujian Fungsional | Menjalankan test case fungsional |
| Eksekusi Pengujian Keamanan | Menjalankan test case security |
| Analisis Hasil & Pelaporan | Dokumentasi temuan dan penulisan laporan |

---

## 10. DAFTAR FITUR YANG DIUJI

| ID Fitur | Nama Fitur | Prioritas |
|---|---|---|
| F-01 | Login dengan kredensial valid | High |
| F-02 | Login dengan kredensial tidak valid | High |
| F-03 | Proteksi halaman tanpa sesi | High |
| F-04 | Tampilan daftar kontak | Medium |
| F-05 | Tambah kontak baru | High |
| F-06 | Edit kontak | High |
| F-07 | Hapus kontak | High |
| F-08 | Logout / Keluar sesi | High |
| F-09 | Upload foto profil (valid) | Medium |
| F-10 | Upload foto profil (tidak valid) | Medium |
| S-01 | SQL Injection pada form login | Critical |
| S-02 | XSS pada vpage.php | High |
| S-03 | Bypass file upload via ekstensi | High |
| S-04 | Akses halaman tanpa autentikasi | High |
| S-05 | Hardcoded credentials | Medium |
| S-06 | Session fixation / hijacking | High |
| S-07 | IDOR (Insecure Direct Object Reference) | High |

---

*Dokumen ini dibuat sebagai bagian dari Ujian Akhir Semester Mata Kuliah Pengujian Perangkat Lunak*
