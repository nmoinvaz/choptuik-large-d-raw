@echo off
rem T16b (1): hier.py M 5 full solve to convergence, 2 processes, below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15-wt\solver\inner_stokes"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hier.py 5 2.71871 0.999087 --x=0.149260325,0.014725513,0.008411409,0.001471486 --procs 2 > hier_M5_full.log 2>&1
echo exit %ERRORLEVEL% >> t16b_1.exit
