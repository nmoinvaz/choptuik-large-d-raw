@echo off
rem #1025 winb D 18.5: signtest.py's syscheck (rebuilds the record's discrete system: |F| within 1% and equal steps, then exits), BelowNormal, 2 threads
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "OPENBLAS_NUM_THREADS=2"
set "OMP_NUM_THREADS=2"
set "MKL_NUM_THREADS=2"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\choptuik-i1025-lowd\solver\matter
start "sys185" /belownormal /wait /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:/Users/nathan/Source/p4hi_1025/raw/I1025-mac/signtest.py C:/Users/nathan/Source/p4hi_1025/raw/I1025-mac/d18/sol_l1kc63Wm1025_D18.500000.npy 18.5 63 around=C:/Users/nathan/Source/p4hi_1025/I1025-win/p4_highD/stub_d185_l1kc63Wm1025_D18.5_leapline.jsonl:18.5:0.02 syscheck > C:\Users\nathan\Source\p4hi_1025\smoke_syscheck_d185.log 2>&1
echo exit %errorlevel% >> C:\Users\nathan\Source\p4hi_1025\smoke_syscheck_d185.log
