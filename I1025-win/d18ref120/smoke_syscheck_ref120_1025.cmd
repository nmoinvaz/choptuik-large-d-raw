@echo off
rem #1025 winb, lambda 1.20: signtest.py's syscheck (rebuilds the record's discrete system: |F| within 1% and equal steps, then exits) for D 18 and D 18.0625, BelowNormal, 2 threads
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "OPENBLAS_NUM_THREADS=2"
set "OMP_NUM_THREADS=2"
set "MKL_NUM_THREADS=2"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\choptuik-i1025-lowd\solver\matter
start "s18" /belownormal /wait /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:/Users/nathan/Source/ref120_1025/raw/I1025-mac/signtest.py C:/Users/nathan/Source/ref120_1025/raw/I1025-win/out/sol_l1kc63W1025_D18.000000.npy 18.0 63 around=C:/Users/nathan/Source/ref120_1025/I1025-win/d18ref120/stub_ref120_D18.jsonl:18.0:0 syscheck > C:\Users\nathan\Source\ref120_1025\smoke_syscheck_D18.log 2>&1
echo exit %errorlevel% >> C:\Users\nathan\Source\ref120_1025\smoke_syscheck_D18.log
start "s180" /belownormal /wait /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:/Users/nathan/Source/ref120_1025/raw/I1025-mac/signtest.py C:/Users/nathan/Source/ref120_1025/raw/I1025-mac/d18/sol_l1kc63Wm1025_D18.062500.npy 18.0625 63 around=C:/Users/nathan/Source/ref120_1025/I1025-win/d18ref120/stub_ref120_D18.0625.jsonl:18.0625:0 syscheck > C:\Users\nathan\Source\ref120_1025\smoke_syscheck_D18.0625.log 2>&1
echo exit %errorlevel% >> C:\Users\nathan\Source\ref120_1025\smoke_syscheck_D18.0625.log
