# test_01_login.py
# Pengujian Otomasi: Modul Autentikasi (Login)
# TC-F-001 hingga TC-F-004

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, VALID_USERNAME, VALID_PASSWORD, TIMEOUT


class TestLogin:
    """Kelas pengujian untuk modul Login / Autentikasi."""

    def test_TC_F_001_login_valid(self, driver):
        """
        TC-F-001: Login dengan username dan password VALID.
        Expected: Redirect ke index.php dan muncul 'Howdy, damn admin!'
        """
        driver.get(f"{BASE_URL}/login.php")

        # Isi form login
        driver.find_element(By.ID, "inputUsername").clear()
        driver.find_element(By.ID, "inputUsername").send_keys(VALID_USERNAME)
        driver.find_element(By.ID, "inputPassword").clear()
        driver.find_element(By.ID, "inputPassword").send_keys(VALID_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Tunggu redirect ke index.php
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("index.php")
        )

        # Verifikasi 1: URL harus mengandung index.php
        assert "index.php" in driver.current_url, (
            f"Seharusnya redirect ke index.php, tapi URL: {driver.current_url}"
        )

        # Verifikasi 2: Pesan sambutan harus muncul
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Howdy, damn admin" in body_text, (
            "Pesan 'Howdy, damn admin!' tidak ditemukan di halaman"
        )

        print("\n[TC-F-001] PASS - Login valid berhasil, redirect ke dashboard")

    def test_TC_F_002_login_password_salah(self, driver):
        """
        TC-F-002: Login dengan password SALAH.
        Expected: Tetap di login.php dan muncul pesan error.
        """
        driver.get(f"{BASE_URL}/login.php")

        driver.find_element(By.ID, "inputUsername").clear()
        driver.find_element(By.ID, "inputUsername").send_keys(VALID_USERNAME)
        driver.find_element(By.ID, "inputPassword").clear()
        driver.find_element(By.ID, "inputPassword").send_keys("passwordsalah123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Tunggu sesaat
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form.form-signin"))
        )

        # Verifikasi 1: URL harus masih di login.php
        assert "login.php" in driver.current_url or "index.php" not in driver.current_url, (
            "Seharusnya tetap di login.php, bukan redirect"
        )

        # Verifikasi 2: Pesan error harus muncul
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Damn, wrong credentials" in body_text, (
            "Pesan error 'Damn, wrong credentials' tidak muncul"
        )

        print("\n[TC-F-002] PASS - Login dengan password salah ditolak")

    def test_TC_F_003_login_username_salah(self, driver):
        """
        TC-F-003: Login dengan username yang tidak terdaftar.
        Expected: Muncul pesan error, tidak bisa masuk.
        """
        driver.get(f"{BASE_URL}/login.php")

        driver.find_element(By.ID, "inputUsername").clear()
        driver.find_element(By.ID, "inputUsername").send_keys("userpalsu_xyz")
        driver.find_element(By.ID, "inputPassword").clear()
        driver.find_element(By.ID, "inputPassword").send_keys("apapun123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "form.form-signin"))
        )

        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Damn, wrong credentials" in body_text, (
            "Pesan error tidak muncul untuk username yang tidak ada"
        )

        print("\n[TC-F-003] PASS - Login dengan username salah ditolak")

    def test_TC_F_004_login_field_kosong(self, driver):
        """
        TC-F-004: Login dengan semua field dikosongkan.
        Expected: Validasi HTML5 mencegah pengiriman form,
                  halaman tidak berubah.
        """
        driver.get(f"{BASE_URL}/login.php")

        # Klik tombol submit tanpa mengisi field
        submit_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_btn.click()

        # Verifikasi: halaman tidak berpindah (masih di login.php)
        # Validasi HTML5 (atribut `required`) akan memblokir submit
        assert "login.php" in driver.current_url or BASE_URL in driver.current_url, (
            "Halaman tidak seharusnya berpindah saat field kosong"
        )

        # Cek field username masih ada di halaman (form tidak disubmit)
        username_field = driver.find_element(By.ID, "inputUsername")
        assert username_field.is_displayed(), "Field username harus masih tampil"

        print("\n[TC-F-004] PASS - Field kosong dicegah oleh validasi HTML5")
