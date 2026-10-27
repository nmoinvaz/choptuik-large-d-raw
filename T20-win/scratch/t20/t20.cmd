@echo off
rem T20: sigma_8 across omega (K 17 phys scan, 4 new omegas plus the reused w_inf), crossing and zero analysis.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\hp-wt\solver\inner_amp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
if not exist scan17phys mkdir scan17phys
copy /y data\sigF_w1.0000_K17_J750_phys.json scan17phys\sigF_w1.00000_K17_J750.json
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u scan_omega.py 0.98 1.02 5 17 750 2 scan17phys 640 --fit phys --mf 6:12 --fit-step 1 > scan17phys.log 2>&1
echo exit %ERRORLEVEL% >> t20_scan.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" arg_crossing.py scan17phys > scan17phys\crossing.txt 2>&1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" zero_selection.py scan17phys > scan17phys\zero.txt 2>&1
echo exit %ERRORLEVEL% >> t20_an.exit
