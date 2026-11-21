@echo off
rem #1025 winb, the k_c 55 test at D 18: signtest.py's syscheck (rebuilds the record's discrete system: |F| within 1% and equal steps, then exits), BelowNormal, 2 threads
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "OPENBLAS_NUM_THREADS=2"
set "OMP_NUM_THREADS=2"
set "MKL_NUM_THREADS=2"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\choptuik-i1025-lowd\solver\matter
start "s55" /belownormal /wait /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:/Users/nathan/Source/kc55_1025/raw/I1025-mac/signtest.py C:/Users/nathan/Source/kc55_1025/raw/I1025-mac/out/sol_l1kc55F1025_D18.000000.npy 18.0 55 around=C:/Users/nathan/Source/kc55_1025/I1025-win/kc55_d18/stub_kc55_D18.jsonl:18.0:0 syscheck > C:\Users\nathan\Source\kc55_1025\smoke_syscheck_kc55.log 2>&1
echo exit %errorlevel% >> C:\Users\nathan\Source\kc55_1025\smoke_syscheck_kc55.log
