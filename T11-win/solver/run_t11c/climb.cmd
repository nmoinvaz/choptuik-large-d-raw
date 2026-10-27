@echo off
rem T11b climb, x_K 0.65 from D = 30.124 to 40. At most 4 threads: 4 junk workers, NE on 2 threads between them.
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONUNBUFFERED=1
set NE_THREADS=2
set NE_JUNK=4
set NE_NJUNK=18
set NE_JUNK_H=1e-2,3e-3,1e-3
set NE_JUNK_DAMP=1
set NE_JUNK_DAMP_MU=1e-3,1e-2,0.1,0.3,1
set NE_PRED_JUNK0=1
set NE_KS=100
set NE_RK=3
set NE_RK_SEG=1,1,1,1,1,1,1,1,8
set NE_SEED_MAX=30.2
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u ..\scan_ne.py scan_ne65_hi.jsonl 30.1 40 0.8 0.8 0.65 probe_ne65_D 23 >> scan_ne65_hi.log 2>&1
echo exit %ERRORLEVEL% >> scan_ne65_hi.log
