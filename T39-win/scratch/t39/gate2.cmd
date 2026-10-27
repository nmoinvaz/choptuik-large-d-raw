@echo off
rem T39 gate 2: the D = 3.55 M = 96 lift with --jac f64 (new hpkernel build), as the dd lift but tag lowDvhf. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
cd /d "%S%\t39-wt"
set PYTHONPATH=%S%\t39\pkg
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hp/lowD_dd.py hp/data/lowD_dd_local_f64gate.jsonl --start "%S%\t35-wt\hp\data\lowD_states\lowDvh_D3.5500_M80.npz" --Ms 96 --nodes 0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8 --kcs 100 --ks 250 --tol_step 1e-30 --it_max 30 --threads 1 --tag lowDvhf --jac f64 > "%S%\t39\gate2.log" 2>&1
echo exit %ERRORLEVEL% >> "%S%\t39\gate2.exit"
