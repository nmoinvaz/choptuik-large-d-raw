@echo off
rem T15 (c2) kc 63 from the kc 47 seeds with NE_WEAK_TOL 2e-12. Launched at below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15-wt\solver\data"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONUNBUFFERED=1
set NE_RK=2
set NE_STRONG_TOL=2e-8
set NE_THREADS=2
set NE_SEED_MIN=3.7
set NE_LAM_EXTRA=scan_ne6_lowD_kc47.jsonl
set NE_WEAK_TOL=2e-12
set NE_SEED_KC=47
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u ..\scan_ne.py scan_lowD3_kc63.jsonl 4.0 3.3 0.05 0.05 0.6 neB_kc47_rk2_D 63 > "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\c2.log" 2>&1
echo exit %ERRORLEVEL% >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\c2.exit"
