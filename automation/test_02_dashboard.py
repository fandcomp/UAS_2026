# test_02_dashboard.py
# Pengujian Otomasi: Modul Dashboard
# TC-F-005, TC-F-006

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, TIMEOUT


class TestDashboard:
    """Kelas pengujian untuk modul Dashboard."""

    def test_TC_F_005_tampilan_dashboard(self, logged_in):
        """
        TC-F-005: Tampilan tabel kontak di dashboard setelah login.
        Expected: Tabel tampil dengan data, semua kolom ada,
                  menu navigasi tampil.
        """
        driver = logged_in

        # Verifikasi 1: Halaman dashboard berhasil dimuat
        assert "index.php" in driver.current_url or "Dashboard" in driver.title, (
            "Tidak berada di halaman dashboard"
        )

        # Verifikasi 2: Pesan sambutan ada
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Howdy, damn admin" in body_text, "Pesan sambutan tidak ditemukan"

        # Verifikasi 3: Tabel kontak ada
        tabel = driver.find_element(By.ID, "employee")
        assert tabel.is_displayed(), "Tabel kontak tidak tampil"

        # Verifikasi 4: Header kolom tabel ada
        headers = driver.find_elements(By.CSS_SELECTOR, "#employee thead th")
        header_texts = [h.text for h in headers]
        for kolom in ["Name", "Email", "Phone", "Title"]:
            assert kolom in header_texts, f"Kolom '{kolom}' tidak ditemukan di tabel"

        # Verifikasi 5: Ada baris data di tabel
        rows = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        assert len(rows) > 0, "Tabel tidak memiliki data kontak"

        # Verifikasi 6: Menu navigasi ada
        assert driver.find_element(
            By.XPATH, "//a[contains(text(),'Add New Contact')]"
        ).is_displayed(), "Menu 'Add New Contact' tidak tampil"

        print(f"\n[TC-F-005] PASS - Dashboard tampil dengan {len(rows)} kontak")

    def test_TC_F_006_akses_dashboard_tanpa_login(self, driver):
        """
        TC-F-006: Akses halaman dashboard tanpa autentikasi.
        Expected: Redirect ke login.php (proteksi sesi berjalan).
        """
        # Buka halaman logout dulu untuk memastikan tidak ada sesi aktif
        driver.get(f"{BASE_URL}/logout.php")

        # Coba akses index.php langsung
        driver.get(f"{BASE_URL}/index.php")

        WebDriverWait(driver, TIMEOUT).until(
            lambda d: "login.php" in d.current_url or "form-signin" in d.page_source
        )

        # Verifikasi: harus diarahkan ke login.php
        assert "login.php" in driver.current_url, (
            f"Seharusnya redirect ke login.php, tapi URL: {driver.current_url}"
        )

        print("\n[TC-F-006] PASS - Dashboard terproteksi, redirect ke login.php")
