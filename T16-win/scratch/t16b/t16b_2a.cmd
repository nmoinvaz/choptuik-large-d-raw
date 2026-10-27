@echo off
rem T16b (2a): hier.py M 5 fixA at w 1.05, then 0.95, 2 processes. Launched at below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15-wt\solver\inner_stokes"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hier.py 5 2.72 1.05 --fixA --x=0.149215713,0.014707521,0.008402341,0.001468584 --procs 2 > hier_M5_fixA_w105.log 2>&1
echo exit %ERRORLEVEL% >> t16b_2a1.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hier.py 5 2.72 0.95 --fixA --x=0.149215713,0.014707521,0.008402341,0.001468584 --procs 2 > hier_M5_fixA_w095.log 2>&1
echo exit %ERRORLEVEL% >> t16b_2a2.exit
