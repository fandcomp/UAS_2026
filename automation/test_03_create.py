# test_03_create.py
# Pengujian Otomasi: Modul Tambah Kontak (Create)
# TC-F-007, TC-F-008

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, TEST_CONTACT, TIMEOUT


class TestCreateContact:
    """Kelas pengujian untuk modul Tambah Kontak."""

    def test_TC_F_007_tambah_kontak_valid(self, logged_in):
        """
        TC-F-007: Tambah kontak baru dengan semua data valid.
        Expected: Kontak tersimpan, redirect ke index.php,
                  kontak baru muncul di daftar.
        """
        driver = logged_in

        # Klik tombol "Add New Contact"
        driver.find_element(
            By.XPATH, "//a[contains(text(),'Add New Contact')]"
        ).click()

        # Tunggu halaman create.php
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("create.php")
        )
        assert "create.php" in driver.current_url

        # Isi form tambah kontak
        driver.find_element(By.ID, "name").clear()
        driver.find_element(By.ID, "name").send_keys(TEST_CONTACT["name"])

        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "email").send_keys(TEST_CONTACT["email"])

        driver.find_element(By.ID, "phone").clear()
        driver.find_element(By.ID, "phone").send_keys(TEST_CONTACT["phone"])

        driver.find_element(By.ID, "title").clear()
        driver.find_element(By.ID, "title").send_keys(TEST_CONTACT["title"])

        # Klik tombol Save
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Tunggu redirect ke index.php
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("index.php")
        )

        # Verifikasi: redirect ke dashboard
        assert "index.php" in driver.current_url, "Tidak redirect ke index.php setelah save"

        # Verifikasi: nama kontak baru muncul di tabel
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert TEST_CONTACT["name"] in body_text, (
            f"Kontak '{TEST_CONTACT['name']}' tidak ditemukan di dashboard"
        )

        print(f"\n[TC-F-007] PASS - Kontak '{TEST_CONTACT['name']}' berhasil ditambahkan")

    def test_TC_F_008_tambah_kontak_field_kosong(self, logged_in):
        """
        TC-F-008: Tambah kontak dengan field Name dikosongkan.
        Expected: Validasi HTML5 mencegah pengiriman, tetap di create.php.
        """
        driver = logged_in
        driver.get(f"{BASE_URL}/create.php")

        # Biarkan field name kosong, isi yang lain
        driver.find_element(By.ID, "email").send_keys("test@email.com")
        driver.find_element(By.ID, "phone").send_keys("08123456789")
        driver.find_element(By.ID, "title").send_keys("Tester")

        # Klik Save tanpa isi Name
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Verifikasi: halaman tidak berpindah (validasi HTML5 aktif)
        assert "create.php" in driver.current_url, (
            "Seharusnya tetap di create.php karena validasi HTML5"
        )

        # Verifikasi: field name masih ada (form tidak disubmit)
        name_field = driver.find_element(By.ID, "name")
        assert name_field.is_displayed()

        print("\n[TC-F-008] PASS - Field kosong dicegah oleh validasi HTML5")
