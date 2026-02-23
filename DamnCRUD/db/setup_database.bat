@echo off
:: setup_database.bat
:: Script otomatis setup database badcrud untuk DamnCRUD
:: Jalankan file ini dengan klik dua kali

title Setup Database - DamnCRUD

echo.
echo  ================================================
echo    SETUP DATABASE DAMNCRUD
echo    Database: badcrud
echo    User    : root / root123
echo  ================================================
echo.

:: ── Cari lokasi MySQL XAMPP ──────────────────────────────
set MYSQL_PATH=C:\xampp\mysql\bin\mysql.exe
set SQL_FILE=%~dp0setup_badcrud.sql

:: Cek apakah MySQL XAMPP ada
if not exist "%MYSQL_PATH%" (
    echo  [!] MySQL tidak ditemukan di: %MYSQL_PATH%
    echo.
    echo  Pilih lokasi MySQL Anda:
    echo    [1] XAMPP default  : C:\xampp\mysql\bin\mysql.exe
    echo    [2] WAMP           : C:\wamp64\bin\mysql\mysql8.0.31\bin\mysql.exe
    echo    [3] Laragon        : C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysql.exe
    echo    [4] Masukkan path manual
    echo.
    set /p pilihan="Pilih (1/2/3/4): "

    if "%pilihan%"=="2" set MYSQL_PATH=C:\wamp64\bin\mysql\mysql8.0.31\bin\mysql.exe
    if "%pilihan%"=="3" set MYSQL_PATH=C:\laragon\bin\mysql\mysql-8.0.30-winx64\bin\mysql.exe
    if "%pilihan%"=="4" (
        set /p MYSQL_PATH="Masukkan path lengkap mysql.exe: "
    )
)

:: ── Verifikasi MySQL ditemukan ───────────────────────────
if not exist "%MYSQL_PATH%" (
    echo.
    echo  [ERROR] File mysql.exe tidak ditemukan di:
    echo          %MYSQL_PATH%
    echo.
    echo  Pastikan XAMPP/WAMP sudah terinstall dan MySQL sudah Start.
    echo  Lalu jalankan script ini lagi.
    pause
    exit /b 1
)

echo  [OK] MySQL ditemukan: %MYSQL_PATH%
echo  [OK] File SQL       : %SQL_FILE%
echo.
echo  Menghubungkan ke MySQL dan membuat database...
echo  (Jika muncul prompt password, tekan Enter saja jika password kosong,
echo   atau ketik password root MySQL Anda)
echo.

:: ── Jalankan SQL ─────────────────────────────────────────
:: Coba dengan password root123 dulu (sesuai functions.php)
"%MYSQL_PATH%" -u root -proot123 < "%SQL_FILE%"

if %errorlevel% == 0 (
    echo.
    echo  ================================================
    echo    [SUKSES] Database badcrud berhasil dibuat!
    echo.
    echo    - Tabel contacts : berisi 13 data kontak
    echo    - Tabel users    : username=admin, pass=nimda666!
    echo  ================================================
    echo.
    echo  Sekarang buka browser dan akses:
    echo  http://localhost/DamnCRUD/login.php
    echo.
) else (
    echo.
    echo  [!] Gagal dengan password root123.
    echo      Mencoba tanpa password...
    echo.
    "%MYSQL_PATH%" -u root < "%SQL_FILE%"

    if %errorlevel% == 0 (
        echo.
        echo  ================================================
        echo    [SUKSES] Database berhasil dibuat tanpa password!
        echo  ================================================
        echo.
        echo  PERHATIAN: Password MySQL Anda kosong, tapi
        echo  functions.php menggunakan password 'root123'.
        echo  Ikuti petunjuk di bawah untuk menyesuaikan.
        echo.
    ) else (
        echo.
        echo  [ERROR] Koneksi MySQL gagal.
        echo.
        echo  Kemungkinan penyebab:
        echo    1. MySQL belum dijalankan di XAMPP
        echo    2. Password root MySQL berbeda
        echo.
        echo  Coba cara manual: lihat PANDUAN_MANUAL_DB.md
        echo.
    )
)

pause
