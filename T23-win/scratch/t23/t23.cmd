@echo off
rem T23: K 21 phys omega scan at wf 0.99, 1.00, 1.01 (2 at a time), then crossing and zero analysis. Below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\hp-wt\solver\inner_amp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
if not exist scan21phys mkdir scan21phys
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u scan_omega.py 0.99 1.01 3 21 750 2 scan21phys 640 --fit phys --mf 6:12 --fit-step 1 > scan21phys.log 2>&1
echo exit %ERRORLEVEL% >> t23_scan.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" arg_crossing.py scan21phys > scan21phys\crossing.txt 2>&1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" zero_selection.py scan21phys > scan21phys\zero.txt 2>&1
echo exit %ERRORLEVEL% >> t23_an.exit
