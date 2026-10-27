@echo off
rem T26: hier.py M 7 fixed-A --predict --floor --verbose=2, 2 processes, below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15-wt\solver\inner_stokes"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hier.py 7 2.72 1.0 --fixA --predict --floor --verbose=2 --x=0.149215713,0.014707521,0.008402341,0.001468584 --procs 2 > hier_M7_fixA_floor.log 2>&1
echo exit %ERRORLEVEL% >> t26.exit
