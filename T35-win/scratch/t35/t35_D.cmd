@echo off
rem T35 part D: the maximum of Delta in double-double, M = 80 from D = 3.7 up to 3.80 on A's nodes. Below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t35-wt"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hp/lowD_dd.py hp/data/lowD_dd_local_max.jsonl --start hp/data/lowD_states/lowDv_D3.7000_M80.npz --nodes 0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8 --Ms 80 --kcs 100 --ks 250 --tol_step 1e-30 --it_max 30 --threads 1 --tag lowDv --resume --Dlist 3.72,3.74,3.75,3.76,3.78,3.80 > hp/data/lowD_logs/local_D.log 2>&1
echo exit %ERRORLEVEL% >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t35\D.exit"
