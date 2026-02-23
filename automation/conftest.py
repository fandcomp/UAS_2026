# conftest.py - Konfigurasi global pytest dan fixture Selenium

import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import BASE_URL, VALID_USERNAME, VALID_PASSWORD, TIMEOUT

# Deteksi environment CI (GitHub Actions set CI=true)
IS_CI = os.environ.get('CI', '').lower() in ('true', '1', 'yes')


def pytest_configure(config):
    """Konfigurasi metadata laporan HTML."""
    config._metadata = {
        "Proyek"      : "DamnCRUD - CRUD Web Application",
        "Mata Kuliah" : "Pengujian Perangkat Lunak",
        "Base URL"    : BASE_URL,
        "Browser"     : "Google Chrome" + (" (headless)" if IS_CI else ""),
        "Framework"   : "Selenium + pytest",
        "Environment" : "CI/GitHub Actions" if IS_CI else "Local",
    }


@pytest.fixture(scope="session")
def driver():
    """
    Fixture utama: membuat satu instance WebDriver Chrome per worker.
    - Mode lokal : Chrome window biasa
    - Mode CI    : Chrome headless (tidak ada tampilan grafis)
    scope="session" → driver hanya dibuka/ditutup sekali per sesi pytest/worker.
    """
    chrome_options = Options()

    if IS_CI:
        # Mode headless untuk CI (tidak ada display server di GitHub Actions)
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1920,1080")
    else:
        chrome_options.add_argument("--start-maximized")

    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # Selenium Manager bawaan (Selenium 4.6+) mengelola ChromeDriver otomatis
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Ambil screenshot otomatis saat test gagal (berguna di CI)."""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Coba ambil driver dari fixture yang tersedia di test ini
        driver_obj = None
        for fixture_name in ("logged_in", "driver"):
            driver_obj = item.funcargs.get(fixture_name)
            if driver_obj is not None:
                break

        if driver_obj is not None:
            try:
                os.makedirs("screenshots", exist_ok=True)
                safe_name = item.name.replace("[", "_").replace("]", "_")
                screenshot_path = f"screenshots/{safe_name}.png"
                driver_obj.save_screenshot(screenshot_path)
                print(f"\n[SCREENSHOT] Saved: {screenshot_path}")
            except Exception as e:
                print(f"\n[SCREENSHOT] Failed to save: {e}")


def pytest_html_report_title(report):
    """Ubah judul laporan HTML."""
    report.title = "Laporan Hasil Pengujian Otomasi - DamnCRUD"
