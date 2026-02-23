# test_07_logout.py
# Pengujian Otomasi: Modul Logout
# TC-F-015

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, TIMEOUT


class TestLogout:
    """Kelas pengujian untuk modul Logout."""

    def test_TC_F_015_logout_dari_aplikasi(self, logged_in):
        """
        TC-F-015: Logout dari aplikasi dan verifikasi sesi berakhir.
        Expected:
          1. Klik Sign out → redirect ke login.php
          2. Setelah logout, akses index.php → redirect ke login.php
        """
        driver = logged_in

        # Verifikasi sedang di halaman yang terautentikasi
        assert "index.php" in driver.current_url

        # Klik tombol "Sign out" di menu
        driver.find_element(
            By.XPATH, "//a[contains(text(),'Sign out') or contains(text(),'sign out')]"
        ).click()

        # Tunggu redirect ke login.php
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("login.php")
        )

        # Verifikasi 1: berhasil ke halaman login
        assert "login.php" in driver.current_url, (
            f"Seharusnya redirect ke login.php, tapi: {driver.current_url}"
        )

        # Verifikasi 2: coba akses dashboard setelah logout
        driver.get(f"{BASE_URL}/index.php")
        WebDriverWait(driver, TIMEOUT).until(
            lambda d: "login.php" in d.current_url or "form-signin" in d.page_source
        )

        # Harus diarahkan kembali ke login.php (sesi sudah dihapus)
        assert "login.php" in driver.current_url, (
            "Sesi masih aktif setelah logout - ini adalah celah keamanan!"
        )

        print("\n[TC-F-015] PASS - Logout berhasil, sesi tidak aktif lagi")
