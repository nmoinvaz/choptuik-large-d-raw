@echo off
rem T18: K 11 J 1000 omega scan near omega_inf (11 omegas, 6 at a time), then arg_crossing on it and on scan13b.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15-wt\solver\inner_amp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u scan_omega.py 0.96 1.06 11 11 1000 6 scan11f > scan11f.log 2>&1
echo exit %ERRORLEVEL% >> t18_scan.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" arg_crossing.py scan11f > scan11f\arg.txt 2>&1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" arg_crossing.py scan13b > scan13b\arg.txt 2>&1
echo exit %ERRORLEVEL% >> t18_arg.exit
