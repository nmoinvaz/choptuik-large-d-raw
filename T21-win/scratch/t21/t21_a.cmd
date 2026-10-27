@echo off
rem T21 (wf 0.99, 1.00 on 2 processes): K 19 phys omega scan, below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\hp-wt\solver\inner_amp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
if not exist scan19phys mkdir scan19phys
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u scan_omega.py 0.99 1.00 2 19 750 2 scan19phys 640 --fit phys --mf 6:12 --fit-step 1 >> scan19phys.log 2>&1
echo exit %ERRORLEVEL% >> t21_a.exit
