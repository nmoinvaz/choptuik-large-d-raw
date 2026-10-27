@echo off
rem T19: K 15 phys omega scan (7 omegas, 4 at a time), crossing and zero analysis, then sigma_8 at omega_inf (K 17, 4 procs).
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\hp-wt\solver\inner_amp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u scan_omega.py 0.97 1.03 7 15 750 4 scan15phys 640 --fit phys --mf 6:11 --fit-step 2 > scan15phys.log 2>&1
echo exit %ERRORLEVEL% >> t19_a.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" arg_crossing.py scan15phys > scan15phys\crossing.txt 2>&1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" zero_selection.py scan15phys > scan15phys\zero.txt 2>&1
echo exit %ERRORLEVEL% >> t19_an.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u amp_flint_par.py 1.0 17 750 640 --procs 4 --fit phys --mf 6:12 --fit-step 1 --out data\sigF_w1.0000_K17_J750_phys.json > data\k17_J750_phys.log 2>&1
echo exit %ERRORLEVEL% >> t19_b.exit
