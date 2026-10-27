@echo off
rem T14b: amp_flint_par K 17 at J 1000 and 1500, then the K 13 J 1000 omega scan and zero_selection. 6 processes.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15-wt\solver\inner_amp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u amp_flint_par.py 1.0 17 1000 --procs 6 > k17_J1000.log 2>&1
echo exit %ERRORLEVEL% >> t14b_a.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u amp_flint_par.py 1.0 17 1500 --procs 6 > k17_J1500.log 2>&1
echo exit %ERRORLEVEL% >> t14b_b.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u scan_omega.py 0.70 1.30 13 13 1000 6 scan13b > scan13b.log 2>&1
echo exit %ERRORLEVEL% >> t14b_c.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" zero_selection.py scan13b > zero_scan13b.txt 2>&1
echo exit %ERRORLEVEL% >> t14b_d.exit
