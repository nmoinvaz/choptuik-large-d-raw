@echo off
rem #1025 winb follow-on: signtest.py's syscheck (rebuilds the record's discrete system: |F| within 1% and equal steps, then exits) for rows A and B, BelowNormal, 2 threads, beside P4's row 4
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "OPENBLAS_NUM_THREADS=2"
set "OMP_NUM_THREADS=2"
set "MKL_NUM_THREADS=2"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\choptuik-i1025-lowd\solver\matter
start "sysA" /belownormal /wait /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:/Users/nathan/Source/p4hi_1025/raw/I1025-mac/signtest.py C:/Users/nathan/Source/p4hi_1025/raw/I1025-win/out/sol_l1kc63Fw1025_D17.5000.npy 17.5 63 around=C:/Users/nathan/Source/p4hi_1025/I1025-win/p4_highD/stub_rowA_l1kc63Fw1025_D17.5_trendguess.jsonl:17.5:0.02 syscheck > C:\Users\nathan\Source\p4hi_1025\smoke_syscheck_A.log 2>&1
echo exit A %errorlevel% >> C:\Users\nathan\Source\p4hi_1025\smoke_syscheck_A.log
start "sysB" /belownormal /wait /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:/Users/nathan/Source/p4hi_1025/raw/I1025-mac/signtest.py C:/Users/nathan/Source/p4hi_1025/raw/I1025-win/out/sol_l1kc63W1025_D17.750000.npy 17.75 63 around=C:/Users/nathan/Source/p4hi_1025/I1025-win/p4_highD/stub_rowB_l1kc63W1025_D17.75_leapline.jsonl:17.75:0.02 syscheck > C:\Users\nathan\Source\p4hi_1025\smoke_syscheck_B.log 2>&1
echo exit B %errorlevel% >> C:\Users\nathan\Source\p4hi_1025\smoke_syscheck_B.log
