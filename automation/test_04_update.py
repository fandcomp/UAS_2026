# test_04_update.py
# Pengujian Otomasi: Modul Edit Kontak (Update)
# TC-F-009, TC-F-010, TC-F-011, TC-F-012

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, UPDATE_CONTACT, TIMEOUT


class TestUpdateContact:
    """Kelas pengujian untuk modul Edit Kontak."""

    def test_TC_F_009_edit_kontak_valid(self, logged_in):
        """
        TC-F-009: Edit kontak pertama dengan data baru.
        Expected: Data ter-update, redirect ke index.php.
        """
        driver = logged_in
        driver.get(f"{BASE_URL}/index.php")

        # Klik tombol Edit pada kontak pertama di tabel
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.btn-success"))
        )
        edit_btn = driver.find_elements(By.CSS_SELECTOR, "a.btn-success")[0]
        edit_btn.click()

        # Tunggu halaman update.php
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("update.php")
        )
        assert "update.php" in driver.current_url

        # Update field Name
        name_field = driver.find_element(By.ID, "name")
        name_field.clear()
        name_field.send_keys(UPDATE_CONTACT["name"])

        # Update field Title
        title_field = driver.find_element(By.ID, "title")
        title_field.clear()
        title_field.send_keys(UPDATE_CONTACT["title"])

        # Klik Update
        driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

        # Tunggu redirect ke index.php
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("index.php")
        )

        # Verifikasi: redirect ke dashboard
        assert "index.php" in driver.current_url

        # Verifikasi: nama baru muncul di tabel
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert UPDATE_CONTACT["name"] in body_text, (
            f"Nama yang diupdate '{UPDATE_CONTACT['name']}' tidak muncul di tabel"
        )

        print(f"\n[TC-F-009] PASS - Kontak berhasil diubah menjadi '{UPDATE_CONTACT['name']}'")

    def test_TC_F_010_bug_field_phone_kosong(self, logged_in):
        """
        TC-F-010: Verifikasi bug - field phone selalu kosong di form edit.
        Expected (BUG): Field phone kosong meski kontak punya nomor telepon.
        """
        driver = logged_in
        # Edit kontak ID 2 yang pasti punya nomor telepon (David Deacon - 2025550121)
        driver.get(f"{BASE_URL}/update.php?id=2")

        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "phone"))
        )

        phone_field = driver.find_element(By.ID, "phone")
        phone_value = phone_field.get_attribute("value")

        # Catat hasil - ini BUG yang sudah diketahui
        if phone_value == "" or phone_value is None:
            print("\n[TC-F-010] BUG CONFIRMED - Field phone KOSONG meski database memiliki data")
            print("  Root cause: update.php:50 menggunakan value='' bukan value='<?= $contact['phone'] ?>'")
            # Tidak membuat test FAIL karena bug ini sudah diketahui (didokumentasikan)
            pytest.xfail("BUG-002: Field phone tidak menampilkan nilai dari database (update.php:50)")
        else:
            print(f"\n[TC-F-010] Bug sudah diperbaiki - Phone value: {phone_value}")
            assert phone_value != "", "Field phone seharusnya terisi"

    def test_TC_F_011_edit_id_tidak_valid(self, logged_in):
        """
        TC-F-011: Akses halaman edit dengan ID yang tidak ada di database.
        Expected: Muncul teks "Contact doesn't exist!"
        """
        driver = logged_in
        driver.get(f"{BASE_URL}/update.php?id=99999")

        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "Contact doesn" in body_text or "exist" in body_text, (
            "Pesan 'Contact doesn't exist!' tidak muncul untuk ID invalid"
        )

        print("\n[TC-F-011] PASS - Pesan error muncul untuk ID yang tidak ada")

    def test_TC_F_012_edit_tanpa_parameter_id(self, logged_in):
        """
        TC-F-012: Akses update.php tanpa parameter id sama sekali.
        Expected: Muncul teks "No ID specified!"
        """
        driver = logged_in
        driver.get(f"{BASE_URL}/update.php")

        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert "No ID specified" in body_text, (
            "Pesan 'No ID specified!' tidak muncul"
        )

        print("\n[TC-F-012] PASS - Pesan error muncul saat tidak ada parameter ID")
