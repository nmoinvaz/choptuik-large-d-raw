@echo off
rem T12: double-double climb past D = 60 under t12_super.py. 4 threads, launched at below-normal priority.
cd /d "%~dp0"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set RAYON_NUM_THREADS=4
set PYTHONUNBUFFERED=1
set DSS_SOLVER_DIR=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\hp-wt\solver
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u t12_super.py "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\hp-wt" "%~dp0." >> super_stdout.log 2>&1
