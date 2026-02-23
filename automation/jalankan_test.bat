@echo off
:: jalankan_test.bat
:: Script untuk menjalankan test otomasi DamnCRUD di Windows
:: Klik dua kali file ini atau jalankan dari Command Prompt

title Otomasi Test - DamnCRUD

echo ============================================
echo   OTOMASI PENGUJIAN - DAMNCRUD APPLICATION
echo   Pengujian Perangkat Lunak / UAS
echo ============================================
echo.

:: Pindah ke folder automation
cd /d "%~dp0"

:: Cek apakah Python tersedia
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan! Pastikan Python sudah terinstall.
    pause
    exit /b 1
)

:: Cek apakah dependensi sudah terinstall
python -c "import selenium" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Menginstall dependensi Python...
    pip install -r requirements.txt
    echo.
)

:: Buat folder reports jika belum ada
if not exist "..\reports" mkdir "..\reports"

echo [INFO] Memulai eksekusi test otomasi...
echo [INFO] Browser Chrome akan terbuka otomatis
echo [INFO] Pastikan XAMPP Apache dan MySQL sudah berjalan!
echo.
echo Pilihan:
echo   [1] Jalankan SEMUA test
echo   [2] Hanya test FUNGSIONAL
echo   [3] Hanya test KEAMANAN
echo   [4] Hanya test LOGIN
echo   [Q] Keluar
echo.
set /p pilihan="Masukkan pilihan (1/2/3/4/Q): "

if /i "%pilihan%"=="1" goto ALL
if /i "%pilihan%"=="2" goto FUNGSIONAL
if /i "%pilihan%"=="3" goto KEAMANAN
if /i "%pilihan%"=="4" goto LOGIN
if /i "%pilihan%"=="Q" goto EXIT

:ALL
echo.
echo [RUNNING] Semua test...
pytest -v --html=..\reports\hasil_pengujian.html --self-contained-html
goto DONE

:FUNGSIONAL
echo.
echo [RUNNING] Test Fungsional...
pytest test_01_login.py test_02_dashboard.py test_03_create.py test_04_update.py test_05_delete.py test_06_profil.py test_07_logout.py -v --html=..\reports\hasil_fungsional.html --self-contained-html
goto DONE

:KEAMANAN
echo.
echo [RUNNING] Test Keamanan...
pytest test_08_security.py -v --html=..\reports\hasil_keamanan.html --self-contained-html
goto DONE

:LOGIN
echo.
echo [RUNNING] Test Login...
pytest test_01_login.py -v
goto DONE

:DONE
echo.
echo ============================================
echo   TEST SELESAI!
echo   Laporan tersimpan di: ..\reports\
echo ============================================
echo.
echo Buka laporan dengan browser:
echo   ..\reports\hasil_pengujian.html
echo.
pause
goto EXIT

:EXIT
echo Keluar...
