# test_damncrud.py
# ============================================================
# Entry point untuk CI/CD GitHub Actions Pipeline
# Menjalankan 5 test case UAS via pytest-xdist (-n 5)
#
# Implementasi test ada di test_uas_selected.py
# File ini di-import agar CI workflow bisa memanggil:
#   pytest test_damncrud.py -n 5
# ============================================================

from test_uas_selected import (
    TestTC_F_001_LoginValid,
    TestTC_F_005_TampilanDashboard,
    TestTC_F_006_AksesTanpaLogin,
    TestTC_F_007_TambahKontakValid,
    TestTC_F_016_UploadFotoJPG,
)

__all__ = [
    "TestTC_F_001_LoginValid",
    "TestTC_F_005_TampilanDashboard",
    "TestTC_F_006_AksesTanpaLogin",
    "TestTC_F_007_TambahKontakValid",
    "TestTC_F_016_UploadFotoJPG",
]
