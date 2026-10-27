@echo off
rem T16 (a) fixedA M 5, then (b) full_M M 5. 4 processes, launched at below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15-wt\solver\inner_stokes"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u fixedA.py 5 1.0 --procs 4 > fixedA_M5.log 2>&1
echo exit %ERRORLEVEL% >> t16_a.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u full_M.py 5 2.726476 1.015603 0.144419 0.011089 --procs 4 > full_M5.log 2>&1
echo exit %ERRORLEVEL% >> t16_b.exit
