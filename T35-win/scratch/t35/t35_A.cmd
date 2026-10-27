@echo off
rem T35 part A: double-double M = 96 at D = 3.7, then the chain to D = 3.3 (notes/LOW_D.md section 7). Below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t35-wt"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hp/lowD_dd.py hp/data/lowD_dd_local.jsonl --start hp/data/lowD_states/lowDv_D3.7000_M80.npz --nodes 0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8 --Ms 96 --kcs 100 --ks 250 --tol_step 1e-30 --it_max 30 --threads 1 --tag lowDv --resume --auto_nodes --Dlist 3.65,3.6,3.55,3.5,3.45,3.4,3.35,3.3 > hp/data/lowD_logs/local_A.log 2>&1
echo exit %ERRORLEVEL% >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t35\A.exit"
