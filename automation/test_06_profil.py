# test_06_profil.py
# Pengujian Otomasi: Modul Profil & Upload Foto
# TC-F-016, TC-F-017

import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, TIMEOUT


# Path file gambar dummy untuk pengujian upload
TEST_DIR = os.path.dirname(os.path.abspath(__file__))


def buat_file_jpeg(nama_file):
    """Membuat file JPEG minimal yang valid untuk testing upload."""
    # JPEG magic bytes (header minimal)
    jpeg_bytes = (
        b'\xFF\xD8\xFF\xE0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
        b'\xFF\xDB\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t'
        b'\x08\n\x0C\x14\r\x0C\x0B\x0B\x0C\x19\x12\x13\x0F\x14\x1D\x1A'
        b'\x1F\x1E\x1D\x1A\x1C\x1C $.\' ",#\x1C\x1C(7),01444\x1F\'9=82<.342\x1E>'
        b'\xFF\xD9'
    )
    path = os.path.join(TEST_DIR, nama_file)
    with open(path, "wb") as f:
        f.write(jpeg_bytes)
    return path


def buat_file_png(nama_file):
    """Membuat file PNG minimal untuk testing validasi ekstensi."""
    # PNG magic bytes
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
        b'\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00'
        b'\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18'
        b'\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    path = os.path.join(TEST_DIR, nama_file)
    with open(path, "wb") as f:
        f.write(png_bytes)
    return path


class TestProfil:
    """Kelas pengujian untuk modul Profil."""

    def test_TC_F_016_upload_foto_jpg_valid(self, logged_in):
        """
        TC-F-016: Upload foto profil dengan file JPEG yang valid.
        Expected: Upload berhasil, redirect kembali ke profil.php.
        """
        driver = logged_in

        # Buat file JPEG sementara
        jpg_path = buat_file_jpeg("test_upload.jpg")

        try:
            # Akses halaman Profil
            driver.get(f"{BASE_URL}/profil.php")
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )

            # Masukkan path file ke input file
            file_input = driver.find_element(By.ID, "formFile")
            file_input.send_keys(jpg_path)

            # Klik tombol Change
            driver.find_element(
                By.CSS_SELECTOR, "button[type='submit']"
            ).click()

            # Tunggu redirect kembali ke profil.php
            WebDriverWait(driver, TIMEOUT).until(
                EC.url_contains("profil.php")
            )

            # Verifikasi: tidak ada pesan error
            body_text = driver.find_element(By.TAG_NAME, "body").text
            assert "Ekstensi tidak diijinkan" not in body_text, (
                "Muncul pesan error untuk file JPG yang valid"
            )
            assert "profil.php" in driver.current_url

            print("\n[TC-F-016] PASS - Upload foto JPEG berhasil")

        finally:
            # Bersihkan file sementara
            if os.path.exists(jpg_path):
                os.remove(jpg_path)

    def test_TC_F_017_upload_file_bukan_jpg(self, logged_in):
        """
        TC-F-017: Upload file PNG (bukan JPG/JPEG).
        Expected: Muncul pesan error ekstensi tidak diijinkan.
        """
        driver = logged_in

        # Buat file PNG sementara
        png_path = buat_file_png("test_upload.png")

        try:
            driver.get(f"{BASE_URL}/profil.php")
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )

            file_input = driver.find_element(By.ID, "formFile")
            file_input.send_keys(png_path)

            driver.find_element(
                By.CSS_SELECTOR, "button[type='submit']"
            ).click()

            # Tunggu halaman reload
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )

            # Verifikasi: pesan error muncul
            body_text = driver.find_element(By.TAG_NAME, "body").text
            assert "Ekstensi tidak diijinkan" in body_text, (
                "Pesan error 'Ekstensi tidak diijinkan' tidak muncul untuk file PNG"
            )

            print("\n[TC-F-017] PASS - File PNG ditolak dengan pesan error yang benar")

        finally:
            if os.path.exists(png_path):
                os.remove(png_path)
