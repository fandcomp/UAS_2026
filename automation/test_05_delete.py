# test_05_delete.py
# Pengujian Otomasi: Modul Hapus Kontak (Delete)
# TC-F-013, TC-F-014

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from config import BASE_URL, TEST_CONTACT, TIMEOUT


class TestDeleteContact:
    """Kelas pengujian untuk modul Hapus Kontak."""

    def test_TC_F_013_hapus_kontak_konfirmasi_ok(self, logged_in):
        """
        TC-F-013: Hapus kontak yang ditambahkan di TC-F-007 (Test Otomasi).
        Expected: Kontak terhapus, redirect ke index.php, kontak tidak ada lagi.
        """
        driver = logged_in
        driver.get(f"{BASE_URL}/index.php")

        # Cari baris yang mengandung nama kontak test otomasi
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#employee tbody tr"))
        )

        # Cari baris yang berisi "Test Otomasi"
        rows = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        target_row = None
        for row in rows:
            if TEST_CONTACT["name"] in row.text or "Test Otomasi" in row.text:
                target_row = row
                break

        if target_row is None:
            # Jika kontak test tidak ada, hapus kontak terakhir di tabel
            target_row = rows[-1]
            target_name = target_row.find_elements(By.TAG_NAME, "td")[1].text
            print(f"\n  Kontak 'Test Otomasi' tidak ditemukan, menghapus: {target_name}")

        # Catat nama kontak yang akan dihapus
        nama_kontak = target_row.find_elements(By.TAG_NAME, "td")[1].text

        # Klik tombol Delete pada baris tersebut
        delete_btn = target_row.find_element(By.CSS_SELECTOR, "a.btn-danger")
        delete_btn.click()

        # Tangani popup konfirmasi - klik OK
        WebDriverWait(driver, TIMEOUT).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()  # Klik OK

        # Tunggu redirect ke index.php
        WebDriverWait(driver, TIMEOUT).until(
            EC.url_contains("index.php")
        )

        # Verifikasi: redirect ke dashboard
        assert "index.php" in driver.current_url

        # Verifikasi: kontak tidak ada lagi di tabel
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert nama_kontak not in body_text, (
            f"Kontak '{nama_kontak}' seharusnya sudah terhapus"
        )

        print(f"\n[TC-F-013] PASS - Kontak '{nama_kontak}' berhasil dihapus")

    def test_TC_F_014_batal_hapus_kontak(self, logged_in):
        """
        TC-F-014: Klik delete lalu pilih Cancel di dialog konfirmasi.
        Expected: Kontak tidak terhapus, tetap di halaman dashboard.
        """
        driver = logged_in
        driver.get(f"{BASE_URL}/index.php")

        # Hitung jumlah baris sebelum aksi
        WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#employee tbody tr"))
        )
        rows_sebelum = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        jumlah_sebelum = len(rows_sebelum)

        # Ambil nama kontak pertama
        nama_pertama = rows_sebelum[0].find_elements(By.TAG_NAME, "td")[1].text

        # Klik tombol Delete pada kontak pertama
        delete_btn = rows_sebelum[0].find_element(By.CSS_SELECTOR, "a.btn-danger")
        delete_btn.click()

        # Tangani popup konfirmasi - klik CANCEL
        WebDriverWait(driver, TIMEOUT).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.dismiss()  # Klik Cancel

        # Verifikasi: tetap di halaman yang sama
        assert "index.php" in driver.current_url

        # Verifikasi: kontak masih ada
        body_text = driver.find_element(By.TAG_NAME, "body").text
        assert nama_pertama in body_text, (
            f"Kontak '{nama_pertama}' seharusnya masih ada setelah Cancel"
        )

        # Verifikasi: jumlah baris tidak berkurang
        rows_sesudah = driver.find_elements(By.CSS_SELECTOR, "#employee tbody tr")
        assert len(rows_sesudah) == jumlah_sebelum, (
            "Jumlah kontak berkurang padahal penghapusan dibatalkan"
        )

        print(f"\n[TC-F-014] PASS - Kontak tidak terhapus setelah Cancel, "
              f"masih ada {len(rows_sesudah)} kontak")
