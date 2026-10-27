@echo off
rem T28: K 27 J 1000 phys omega scan at wf 0.99, 1.00, 1.01 (%1 at a time), then crossing and zero analysis. Below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\hp-wt\solver\inner_amp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
if not exist scan27J1000 mkdir scan27J1000
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u scan_omega.py 0.99 1.01 3 27 1000 %1 scan27J1000 640 --fit phys --mf 6:12 --fit-step 1 > scan27J1000.log 2>&1
echo exit %ERRORLEVEL% >> t28_scan.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" arg_crossing.py scan27J1000 > scan27J1000\crossing.txt 2>&1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" zero_selection.py scan27J1000 > scan27J1000\zero.txt 2>&1
echo exit %ERRORLEVEL% >> t28_an.exit
