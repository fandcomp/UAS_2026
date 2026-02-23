@echo off
:: jalankan_5_tc.bat
:: Script untuk menjalankan 5 Test Case terpilih UAS
::   TC-F-001  Login dengan Username dan Password Valid
::   TC-F-005  Tampilan Dashboard setelah Login
::   TC-F-006  Akses Dashboard tanpa Login
::   TC-F-007  Tambah Kontak Baru dengan Data Valid
::   TC-F-016  Upload Foto Profil dengan File JPG Valid

title UAS - 5 Test Case Terpilih

cd /d "%~dp0"

echo.
echo  ================================================
echo    UAS - PENGUJIAN PERANGKAT LUNAK
echo    Otomasi 5 Test Case Terpilih - DamnCRUD
echo  ================================================
echo.
echo  Test Case yang akan dijalankan:
echo    [1] TC-F-001  Login Valid
echo    [2] TC-F-005  Tampilan Dashboard
echo    [3] TC-F-006  Akses Dashboard tanpa Login
echo    [4] TC-F-007  Tambah Kontak Baru
echo    [5] TC-F-016  Upload Foto JPG
echo.
echo  PASTIKAN sebelum memulai:
echo    - XAMPP Apache sudah Start
echo    - XAMPP MySQL sudah Start
echo    - Database 'badcrud' sudah diimport
echo    - Aplikasi bisa diakses di http://localhost:8080/DamnCRUD/
echo.
pause

:: Buat folder laporan jika belum ada
if not exist "..\reports" mkdir "..\reports"

echo.
echo  Menjalankan test... Chrome akan terbuka otomatis.
echo.

python -m pytest test_uas_selected.py -v -s ^
    --html=..\reports\hasil_5_tc.html

echo.
echo  ================================================
echo    SELESAI! Laporan tersimpan di:
echo    reports\hasil_5_tc.html
echo  ================================================
echo.
pause
