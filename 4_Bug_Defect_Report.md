# DEFECT / BUG REPORT
## Aplikasi DamnCRUD - Ringkasan Temuan
### Ujian Akhir Semester - Pengujian Perangkat Lunak

---

| Informasi | Detail |
|---|---|
| Tanggal | 23 Februari 2026 |
| Aplikasi | DamnCRUD v1.0 |
| Total Defect | 14 (4 Bug Fungsional + 10 Security Vulnerability) |

---

## A. BUG FUNGSIONAL

---

### BUG-001 | Severity: LOW

| Field | Detail |
|---|---|
| **Judul** | Undefined Variable `$id` pada Tambah Kontak |
| **File & Baris** | `create.php:17` |
| **Status** | Open |
| **Reproduksi** | Tambah kontak baru → klik Save |

**Deskripsi:**
Variabel `$id` tidak pernah dideklarasikan di `create.php` sebelum dimasukkan ke array `execute()`.

**Kode Bermasalah:**
```php
// Baris 16-17
$stmt = $pdo->prepare('INSERT INTO contacts VALUES (?, ?, ?, ?, ?, ?)');
$stmt->execute([$id, $name, $email, $phone, $title, $created]);
//              ^^ Undefined variable - PHP Notice!
```

**Perilaku Aktual:**
PHP PHP mengirim `null` untuk `$id`. MySQL menerima `null` pada kolom `id AUTO_INCREMENT` dan menggenerate nilai otomatis. Fungsional tetap bekerja namun menghasilkan **PHP Notice** di error log server.

**Perbaikan:**
```php
// Hilangkan $id dari query dan execute:
$stmt = $pdo->prepare('INSERT INTO contacts (name, email, phone, title, created) VALUES (?, ?, ?, ?, ?)');
$stmt->execute([$name, $email, $phone, $title, $created]);
```

---

### BUG-002 | Severity: MEDIUM

| Field | Detail |
|---|---|
| **Judul** | Field Phone Kosong di Form Edit Kontak |
| **File & Baris** | `update.php:50` |
| **Status** | Open |
| **Reproduksi** | Login → Klik Edit pada kontak → Lihat field Phone |

**Deskripsi:**
Field "Phone number" tidak menampilkan nilai nomor telepon yang sudah tersimpan di database. Field selalu tampil kosong.

**Kode Bermasalah:**
```php
// Baris 50 - value="" tidak menampilkan data dari database
<input class="form-control form-control-sm" placeholder="Phone number"
    type="text" name="phone" value="" id="phone">
```

**Perbandingan dengan field lain (benar):**
```php
// Name field - BENAR:
<input ... name="name" value="<?= $contact['name'] ?>" ...>
// Email field - BENAR:
<input ... name="email" value="<?= $contact['email'] ?>" ...>
// Phone field - SALAH:
<input ... name="phone" value="" ...>  // Seharusnya value="<?= $contact['phone'] ?>"
```

**Dampak:** Jika user menekan "Update" tanpa mengisi ulang nomor phone, data phone akan terhapus (tersimpan sebagai string kosong) di database.

**Perbaikan:**
```php
<input class="form-control form-control-sm" placeholder="Phone number"
    type="text" name="phone" value="<?= $contact['phone'] ?>" id="phone">
```

---

### BUG-003 | Severity: HIGH

| Field | Detail |
|---|---|
| **Judul** | Inkonsistensi Nama Database antara Kode dan SQL |
| **File** | `functions.php:7` dan `db/damncrud.sql:18` |
| **Status** | Open |
| **Reproduksi** | Import damncrud.sql → jalankan aplikasi → aplikasi gagal koneksi |

**Deskripsi:**
Nama database yang digunakan di kode berbeda dengan nama database yang dibuat oleh file SQL.

| File | Nama Database |
|---|---|
| `functions.php` | `badcrud` |
| `db/damncrud.sql` | `damncrud` |

**Dampak:** Pengguna baru yang mengimport `damncrud.sql` akan mendapati aplikasi tidak bisa berjalan karena database `badcrud` tidak ada.

**Perbaikan:** Sinkronkan salah satu. Pilih nama yang konsisten, misalnya ubah `functions.php` menjadi:
```php
$DATABASE_NAME = 'damncrud';  // sesuaikan dengan nama di SQL file
```

---

### BUG-004 | Severity: HIGH (Security)

| Field | Detail |
|---|---|
| **Judul** | Tidak Ada Pengecekan Sesi di update.php |
| **File** | `update.php` |
| **Status** | Open |
| **Reproduksi** | Tanpa login, akses `update.php?id=1` di browser baru |

**Deskripsi:**
Semua halaman lain memiliki session check, kecuali `update.php`. Ini memungkinkan siapapun memodifikasi data kontak tanpa autentikasi.

**Perbandingan:**
```php
// Halaman LAIN (benar), contoh index.php:
session_start();
if (!isset($_SESSION['user'])) {
    header("location: login.php");
}

// update.php - TIDAK ADA session check sama sekali!
include 'functions.php';
$pdo = pdo_connect();
// langsung memproses request...
```

**Perbaikan:** Tambahkan di baris pertama `update.php`:
```php
session_start();
if (!isset($_SESSION['user'])) {
    header("location: login.php");
    exit();
}
```

---

## B. KERENTANAN KEAMANAN (SECURITY VULNERABILITIES)

---

### SEC-001 | Severity: ⛔ CRITICAL

| Field | Detail |
|---|---|
| **Judul** | SQL Injection - Authentication Bypass |
| **File & Baris** | `login.php:21` |
| **OWASP** | A03:2021 - Injection |
| **CWE** | CWE-89: SQL Injection |
| **CVSS Score** | 9.8 (Critical) |

**Payload:** `admin" -- ` (di field username)

**Query yang terbentuk:**
```sql
SELECT * FROM users WHERE username = "admin" --" AND password = "..." LIMIT 1
-- Kondisi password diabaikan!
```

**Dampak:** Login tanpa password yang valid → akses penuh ke seluruh data kontak.

---

### SEC-002 | Severity: ⛔ CRITICAL

| Field | Detail |
|---|---|
| **Judul** | SQL Injection - Data Extraction (UNION Attack) |
| **File & Baris** | `login.php:21` |
| **OWASP** | A03:2021 - Injection |

**Payload:** `" UNION SELECT id_user, username, password FROM users -- `

**Dampak:** Dapat mengekstrak seluruh data user termasuk hash password.

---

### SEC-003 | Severity: 🔴 HIGH

| Field | Detail |
|---|---|
| **Judul** | Reflected Cross-Site Scripting (XSS) |
| **File & Baris** | `vpage.php:44` |
| **OWASP** | A03:2021 - Injection |
| **CWE** | CWE-79: XSS |

**Kode Rentan:**
```php
echo ("Your thing is " . $_GET["thing"]);
// Tidak ada sanitasi / encoding
```

**Payload:** `<script>alert('XSS')</script>`

**Dampak:** Eksekusi script di browser korban, pencurian cookie, phishing.

---

### SEC-004 | Severity: 🔴 HIGH

| Field | Detail |
|---|---|
| **Judul** | Broken Access Control - Missing Authentication |
| **File** | `update.php` |
| **OWASP** | A01:2021 - Broken Access Control |

Sudah dijelaskan di BUG-004.

---

### SEC-005 | Severity: 🔴 HIGH

| Field | Detail |
|---|---|
| **Judul** | Insecure Direct Object Reference (IDOR) |
| **File** | `update.php`, `delete.php` |
| **OWASP** | A01:2021 - Broken Access Control |

**Cara Eksploitasi:** Ubah nilai `id` di URL:
- `update.php?id=1` → `update.php?id=5` → modifikasi kontak lain
- `delete.php?id=1` → `delete.php?id=10` → hapus kontak lain

---

### SEC-006 | Severity: 🔴 HIGH

| Field | Detail |
|---|---|
| **Judul** | File Upload - Insufficient Extension Validation |
| **File & Baris** | `profil.php:14-21` |
| **OWASP** | A04:2021 - Insecure Design |

**Payload:** File `webshell.php.jpg` dapat melewati validasi ekstensi.

---

### SEC-007 | Severity: 🟡 MEDIUM

| Field | Detail |
|---|---|
| **Judul** | Hardcoded Database Credentials |
| **File & Baris** | `functions.php:3-7` |
| **OWASP** | A02:2021 - Cryptographic Failures |

**Temuan:** Password `root123` tersimpan plaintext di source code.

---

### SEC-008 | Severity: 🟡 MEDIUM

| Field | Detail |
|---|---|
| **Judul** | Weak Password Hashing (SHA256 + Static Salt) |
| **File & Baris** | `login.php:19-21` |
| **OWASP** | A02:2021 - Cryptographic Failures |

**Temuan:** Menggunakan SHA256 dengan salt statis `XDrBmrW9g2fb`. Seharusnya menggunakan `password_hash()` / bcrypt yang lebih kuat.

---

### SEC-009 | Severity: 🟡 MEDIUM

| Field | Detail |
|---|---|
| **Judul** | Tidak Ada Session Timeout |
| **Semua File** | PHP |
| **OWASP** | A07:2021 - Auth Failures |

Tidak ada mekanisme auto-logout setelah periode tidak aktif.

---

### SEC-010 | Severity: 🟡 MEDIUM

| Field | Detail |
|---|---|
| **Judul** | Cookie Session Tanpa HttpOnly Flag |
| **Semua File** | PHP |
| **OWASP** | A07:2021 - Auth Failures |

Cookie PHPSESSID tidak dikonfigurasi dengan flag `HttpOnly` → rentan terhadap JavasScript cookie theft (memperparah dampak XSS).

---

## C. RINGKASAN STATISTIK

```
Total Defect Ditemukan  : 14
├── Bug Fungsional      :  4
│   ├── Low             :  1 (BUG-001)
│   ├── Medium          :  1 (BUG-002)
│   └── High            :  2 (BUG-003, BUG-004)
└── Security Vulnerability : 10
    ├── Critical        :  2 (SEC-001, SEC-002)
    ├── High            :  4 (SEC-003, SEC-004, SEC-005, SEC-006)
    └── Medium          :  4 (SEC-007, SEC-008, SEC-009, SEC-010)
```

### Status Semua Defect

| ID | Judul | Severity | Status |
|---|---|---|---|
| BUG-001 | Undefined variable $id | Low | Open |
| BUG-002 | Field phone kosong di update | Medium | Open |
| BUG-003 | Inkonsistensi nama database | High | Open |
| BUG-004 | update.php tanpa auth check | High | Open |
| SEC-001 | SQL Injection - Auth Bypass | Critical | Open |
| SEC-002 | SQL Injection - UNION Attack | Critical | Open |
| SEC-003 | Reflected XSS | High | Open |
| SEC-004 | Missing Auth di update.php | High | Open |
| SEC-005 | IDOR | High | Open |
| SEC-006 | File Upload Bypass | High | Open |
| SEC-007 | Hardcoded Credentials | Medium | Open |
| SEC-008 | Weak Password Hashing | Medium | Open |
| SEC-009 | No Session Timeout | Medium | Open |
| SEC-010 | Cookie tanpa HttpOnly | Medium | Open |

---

*Dokumen ini merupakan bagian dari UAS Mata Kuliah Pengujian Perangkat Lunak - Politeknik SSN*
