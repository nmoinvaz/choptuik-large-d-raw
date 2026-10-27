@echo off
rem T22 (a) M 7 fixed-A --schur, then (c) M 7 full --schur. 2 processes, below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15-wt\solver\inner_stokes"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hier.py 7 2.72 1.0 --fixA --schur --verbose=2 --x=0.149215713,0.014707521,0.00844556,0.001508163,0.000475916,0.000121569 --procs 2 > hier_M7_fixA.log 2>&1
echo exit %ERRORLEVEL% >> t22_a.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hier.py 7 2.718585 0.999230 --schur --verbose=2 --procs 2 > hier_M7_full.log 2>&1
echo exit %ERRORLEVEL% >> t22_c.exit
