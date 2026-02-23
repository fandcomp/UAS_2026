# test_uas_selected.py
# ============================================================
# PENGUJIAN OTOMASI - UAS PENGUJIAN PERANGKAT LUNAK
# Aplikasi : DamnCRUD
# Framework: Selenium + pytest
#
# Test Case yang diuji (5 TC):
#   TC-F-001 | Login dengan Username dan Password Valid
#   TC-F-005 | Tampilan Dashboard setelah Login
#   TC-F-006 | Akses Dashboard tanpa Login
#   TC-F-007 | Tambah Kontak Baru dengan Data Valid
#   TC-F-016 | Upload Foto Profil dengan File JPG Valid
# ============================================================

import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, VALID_USERNAME, VALID_PASSWORD, TEST_CONTACT, TIMEOUT


# ── Helper: buat file JPEG minimal di folder yang sama ──────────────────────
def _buat_file_jpeg(nama_file):
    """Membuat file JPEG berukuran minimal yang valid secara format."""
    jpeg_bytes = (
        b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
        b'\xFF\xDB\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t'
        b'\x08\n\x0C\x14\r\x0C\x0B\x0B\x0C\x19\x12\x13\x0F\x14\x1D\x1A'
        b'\x1F\x1E\x1D\x1A\x1C\x1C $.\' ",#\x1C\x1C(7),01444\x1F\'9=82<.342\x1E>'
        b'\xFF\xD9'
    )
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), nama_file)
    with open(path, "wb") as f:
        f.write(jpeg_bytes)
    return path


# ============================================================
# TC-F-001 | Login dengan Username dan Password Valid
# ============================================================
class TestTC_F_001_LoginValid:
    """
    Test Case : TC-F-001
    Nama      : Login dengan Username dan Password Valid
    Modul     : Autentikasi / Login
    Tujuan    : Memverifikasi bahwa pengguna dapat login
                dengan kredensial yang benar dan diarahkan
                ke halaman dashboard.
    """

    def test_login_dengan_username_dan_password_valid(self, driver):
        # ── Langkah 1: Buka halaman login ───────────────────
        driver.get(f"{BASE_URL}/login.php")

        # ── Langkah 2: Isi field Username ───────────────────
        username_field = driver.find_element(By.ID, "inputUsername")
        username_field.clear()
        username_field.send_keys(VALID_USERNAME)          # "admin"

        # ── Langkah 3: Isi field Password ───────────────────
        password_field = driver.find_element(By.ID, "inputPassword")
        password_field.clear()
        password_field.send_keys(VALID_PASSWORD)          # "nimda666!"

        # ── Langkah 4: Klik tombol Sign In ──────────────────
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # ── Langkah 5: Tunggu redirect ke dashboard ─────────
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("index.php")
        )

        # ── Verifikasi 1: URL harus mengandung index.php ────
        assert "index.php" in driver.current_url, (
            f"[FAIL] Seharusnya redirect ke index.php\n"
            f"       URL aktual: {driver.current_url}"
        )

        # ── Verifikasi 2: Pesan sambutan muncul di halaman ──
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Howdy, damn admin" in body_text, (
            "[FAIL] Pesan 'Howdy, damn admin!' tidak ditemukan di halaman dashboard"
        )

        print(
            "\n╔══════════════════════════════════════════╗"
            "\n║  TC-F-001 : PASS                         ║"
            "\n║  Login valid berhasil → redirect ke      ║"
            "\n║  dashboard, pesan sambutan muncul        ║"
            "\n╚══════════════════════════════════════════╝"
        )


# ============================================================
# TC-F-005 | Tampilan Dashboard setelah Login
# ============================================================
class TestTC_F_005_TampilanDashboard:
    """
    Test Case : TC-F-005
    Nama      : Tampilan Dashboard setelah Login
    Modul     : Dashboard
    Tujuan    : Memverifikasi bahwa setelah login, halaman
                dashboard menampilkan tabel kontak dengan
                semua kolom dan menu navigasi yang benar.
    """

    def test_tampilan_dashboard_setelah_login(self, logged_in):
        driver = logged_in

        # ── Verifikasi 1: Berada di halaman dashboard ───────
        assert "index.php" in driver.current_url, (
            "[FAIL] Tidak berada di halaman index.php"
        )

        # ── Verifikasi 2: Pesan sambutan ada ────────────────
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Howdy, damn admin" in body_text, (
            "[FAIL] Pesan 'Howdy, damn admin!' tidak ditemukan"
        )

        # ── Verifikasi 3: Tabel kontak tampil ───────────────
        tabel = driver.find_element(By.ID, "employee")
        assert tabel.is_displayed(), (
            "[FAIL] Tabel kontak dengan id='employee' tidak tampil"
        )

        # ── Verifikasi 4: Kolom tabel lengkap ───────────────
        headers      = driver.find_elements(By.CSS_SELECTOR, "#employee thead th")
        header_texts = [h.text for h in headers]
        for kolom in ["Name", "Email", "Phone", "Title"]:
            assert kolom in header_texts, (
                f"[FAIL] Kolom '{kolom}' tidak ada di header tabel"
            )

        # ── Verifikasi 5: Tabel berisi data ─────────────────
        rows = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        assert len(rows) > 0, "[FAIL] Tabel tidak memiliki baris data kontak"

        # ── Verifikasi 6: Menu navigasi tampil ──────────────
        menu_add = driver.find_element(
            By.XPATH, "//a[contains(text(),'Add New Contact')]"
        )
        assert menu_add.is_displayed(), (
            "[FAIL] Tombol menu 'Add New Contact' tidak tampil"
        )

        print(
            f"\n╔══════════════════════════════════════════╗"
            f"\n║  TC-F-005 : PASS                         ║"
            f"\n║  Dashboard tampil dengan {len(rows):>2} kontak       ║"
            f"\n║  Kolom: Name, Email, Phone, Title ✓      ║"
            f"\n║  Menu navigasi tampil              ✓      ║"
            f"\n╚══════════════════════════════════════════╝"
        )


# ============================================================
# TC-F-006 | Akses Dashboard tanpa Login
# ============================================================
class TestTC_F_006_AksesTanpaLogin:
    """
    Test Case : TC-F-006
    Nama      : Akses Dashboard tanpa Login
    Modul     : Dashboard / Session Management
    Tujuan    : Memverifikasi bahwa halaman dashboard tidak
                dapat diakses tanpa sesi aktif dan sistem
                mengarahkan ke halaman login.
    """

    def test_akses_dashboard_tanpa_login(self, driver):
        # ── Langkah 1: Hapus sesi aktif dengan logout ───────
        driver.get(f"{BASE_URL}/logout.php")

        # ── Langkah 2: Langsung akses index.php ─────────────
        driver.get(f"{BASE_URL}/index.php")

        # ── Langkah 3: Tunggu redirect ──────────────────────
        WebDriverWait(driver, TIMEOUT).until(
            lambda d: "login.php" in d.current_url
                      or "form-signin" in d.page_source
        )

        # ── Verifikasi 1: Harus redirect ke login.php ───────
        assert "login.php" in driver.current_url, (
            f"[FAIL] Seharusnya redirect ke login.php\n"
            f"       URL aktual: {driver.current_url}\n"
            f"       → Halaman dashboard dapat diakses tanpa login!"
        )

        # ── Verifikasi 2: Konten dashboard tidak tampil ─────
        assert "Howdy" not in driver.find_element(By.TAG_NAME, "body").text, (
            "[FAIL] Konten dashboard terlihat tanpa login"
        )

        print(
            "\n╔══════════════════════════════════════════╗"
            "\n║  TC-F-006 : PASS                         ║"
            "\n║  Akses tanpa login → redirect ke         ║"
            "\n║  login.php dengan benar                  ║"
            "\n╚══════════════════════════════════════════╝"
        )


# ============================================================
# TC-F-007 | Tambah Kontak Baru dengan Data Valid
# ============================================================
class TestTC_F_007_TambahKontakValid:
    """
    Test Case : TC-F-007
    Nama      : Tambah Kontak Baru dengan Data Valid
    Modul     : Create Contact
    Tujuan    : Memverifikasi bahwa pengguna dapat menambah
                kontak baru dan kontak tersebut muncul di
                halaman dashboard.
    """

    def test_tambah_kontak_baru_dengan_data_valid(self, logged_in):
        driver = logged_in

        # ── Langkah 1: Klik tombol Add New Contact ──────────
        driver.find_element(
            By.XPATH, "//a[contains(text(),'Add New Contact')]"
        ).click()

        # ── Langkah 2: Tunggu halaman create.php ────────────
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("create.php")
        )
        assert "create.php" in driver.current_url, (
            "[FAIL] Tidak berada di halaman create.php"
        )

        # ── Langkah 3: Isi field Name ────────────────────────
        name_field = driver.find_element(By.ID, "name")
        name_field.clear()
        name_field.send_keys(TEST_CONTACT["name"])        # "Test Otomasi"

        # ── Langkah 4: Isi field Email ───────────────────────
        email_field = driver.find_element(By.ID, "email")
        email_field.clear()
        email_field.send_keys(TEST_CONTACT["email"])      # "test.otomasi@email.com"

        # ── Langkah 5: Isi field Phone ───────────────────────
        phone_field = driver.find_element(By.ID, "phone")
        phone_field.clear()
        phone_field.send_keys(TEST_CONTACT["phone"])      # "081234567890"

        # ── Langkah 6: Isi field Title ───────────────────────
        title_field = driver.find_element(By.ID, "title")
        title_field.clear()
        title_field.send_keys(TEST_CONTACT["title"])      # "QA Engineer"

        # ── Langkah 7: Klik tombol Save ──────────────────────
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # ── Langkah 8: Tunggu redirect ke index.php ──────────
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("index.php")
        )

        # ── Verifikasi 1: Redirect ke dashboard ─────────────
        assert "index.php" in driver.current_url, (
            "[FAIL] Seharusnya redirect ke index.php setelah menyimpan kontak"
        )

        # ── Langkah 9: Reload halaman agar data terbaru muncul
        driver.refresh()
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "employee"))
        )

        # ── Langkah 10: Ketik nama kontak di search bar DataTable
        search_box = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#employee_filter input[type='search']"))
        )
        search_box.clear()
        search_box.send_keys(TEST_CONTACT["name"])

        # ── Langkah 11: Tunggu baris hasil filter muncul ─────
        # DataTable akan menampilkan hanya baris yang cocok
        kontak_row = WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//table[@id='employee']//td[contains(text(),'{TEST_CONTACT['name']}')]")
            )
        )

        # ── Verifikasi 2: Baris kontak terlihat di tabel ─────
        assert kontak_row.is_displayed(), (
            f"[FAIL] Kontak '{TEST_CONTACT['name']}' tidak muncul setelah filter"
        )

        # ── Langkah 12: Klik baris kontak (highlight) ────────
        kontak_row.click()

        print(
            f"\n╔══════════════════════════════════════════╗"
            f"\n║  TC-F-007 : PASS                         ║"
            f"\n║  Kontak '{TEST_CONTACT['name']}' berhasil  ║"
            f"\n║  disimpan dan tampil di dashboard        ║"
            f"\n╚══════════════════════════════════════════╝"
        )


# ============================================================
# TC-F-016 | Upload Foto Profil dengan File JPG Valid
# ============================================================
class TestTC_F_016_UploadFotoJPG:
    """
    Test Case : TC-F-016
    Nama      : Upload Foto Profil dengan File JPG Valid
    Modul     : Profil
    Tujuan    : Memverifikasi bahwa pengguna dapat mengupload
                foto profil berformat JPG/JPEG dan sistem
                menyimpannya tanpa pesan error.
    """

    def test_upload_foto_profil_dengan_file_jpg_valid(self, logged_in):
        driver  = logged_in
        jpg_path = _buat_file_jpeg("foto_test.jpg")

        try:
            # ── Langkah 1: Akses halaman Profil ─────────────
            driver.get(f"{BASE_URL}/profil.php")
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[type='file']")
                )
            )
            assert "profil.php" in driver.current_url, (
                "[FAIL] Tidak berada di halaman profil.php"
            )

            # ── Langkah 2: Pilih file JPG ────────────────────
            file_input = driver.find_element(By.ID, "formFile")
            file_input.send_keys(jpg_path)          # kirim path file ke input

            # ── Langkah 3: Klik tombol Change ───────────────
            driver.find_element(
                By.CSS_SELECTOR, "button[type='submit']"
            ).click()

            # ── Langkah 4: Tunggu redirect kembali ──────────
            WebDriverWait(driver, TIMEOUT).until(
                EC.url_contains("profil.php")
            )

            # ── Verifikasi 1: Tidak ada pesan error ─────────
            body_text = driver.find_element(By.TAG_NAME, "body").text
            assert "Ekstensi tidak diijinkan" not in body_text, (
                "[FAIL] Muncul pesan error 'Ekstensi tidak diijinkan'"
                " padahal file JPG seharusnya diterima"
            )

            # ── Verifikasi 2: Masih berada di profil.php ────
            assert "profil.php" in driver.current_url, (
                "[FAIL] Seharusnya kembali ke profil.php setelah upload"
            )

            # ── Verifikasi 3: Gambar profil tampil ──────────
            img = driver.find_element(By.CSS_SELECTOR, "img[src='image/profile.jpg']")
            assert img.is_displayed(), (
                "[FAIL] Gambar profil tidak tampil setelah upload"
            )

            print(
                "\n╔══════════════════════════════════════════╗"
                "\n║  TC-F-016 : PASS                         ║"
                "\n║  Upload foto JPG berhasil, tidak ada     ║"
                "\n║  pesan error, gambar profil tampil       ║"
                "\n╚══════════════════════════════════════════╝"
            )

        finally:
            # Hapus file sementara yang dibuat untuk test ini
            if os.path.exists(jpg_path):
                os.remove(jpg_path)
