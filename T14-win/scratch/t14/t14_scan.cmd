@echo off
rem T14: omega scan, 13 omegas, K 13, J 500, 5 processes. Launched at below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\hp-wt\solver\inner_amp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u scan_omega.py 0.70 1.30 13 13 500 5 scan13 >> scan13.log 2>&1
echo exit %ERRORLEVEL% >> t14_scan.exit
