@echo off
rem T27: K 27 phys omega scan at wf 0.99, 1.00, 1.01 (3 at once), then crossing and zero analysis. Below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\hp-wt\solver\inner_amp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
if not exist scan27phys mkdir scan27phys
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u scan_omega.py 0.99 1.01 3 27 750 3 scan27phys 640 --fit phys --mf 6:12 --fit-step 1 > scan27phys.log 2>&1
echo exit %ERRORLEVEL% >> t27_scan.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" arg_crossing.py scan27phys > scan27phys\crossing.txt 2>&1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" zero_selection.py scan27phys > scan27phys\zero.txt 2>&1
echo exit %ERRORLEVEL% >> t27_an.exit
