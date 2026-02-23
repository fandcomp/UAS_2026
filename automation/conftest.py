# conftest.py - Konfigurasi global pytest dan fixture Selenium

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import BASE_URL, VALID_USERNAME, VALID_PASSWORD, TIMEOUT


def pytest_configure(config):
    """Konfigurasi metadata laporan HTML."""
    config._metadata = {
        "Proyek"     : "DamnCRUD - CRUD Web Application",
        "Mata Kuliah": "Pengujian Perangkat Lunak",
        "Base URL"   : BASE_URL,
        "Browser"    : "Google Chrome",
        "Framework"  : "Selenium + pytest",
    }


@pytest.fixture(scope="session")
def driver():
    """
    Fixture utama: membuat satu instance WebDriver Chrome.
    Selenium 4.6+ memiliki Selenium Manager bawaan yang otomatis
    mengelola ChromeDriver tanpa perlu webdriver-manager.
    scope="session" → driver hanya dibuka/ditutup sekali per sesi pytest.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Selenium Manager bawaan mengelola ChromeDriver otomatis
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(TIMEOUT)

    yield driver   # driver diserahkan ke test

    driver.quit()  # tutup browser setelah semua test selesai


@pytest.fixture(scope="function")
def logged_in(driver):
    """
    Fixture helper: memastikan driver sudah login sebelum test dijalankan.
    Berguna untuk test yang butuh sesi aktif (CRUD, profil, dll).
    """
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    driver.get(f"{BASE_URL}/login.php")
    driver.find_element("id", "inputUsername").clear()
    driver.find_element("id", "inputUsername").send_keys(VALID_USERNAME)
    driver.find_element("id", "inputPassword").clear()
    driver.find_element("id", "inputPassword").send_keys(VALID_PASSWORD)
    driver.find_element("css selector", "button[type='submit']").click()

    WebDriverWait(driver, TIMEOUT).until(
        EC.url_contains("index.php")
    )
    yield driver


def pytest_html_report_title(report):
    """Ubah judul laporan HTML."""
    report.title = "Laporan Hasil Pengujian Otomasi - DamnCRUD"
