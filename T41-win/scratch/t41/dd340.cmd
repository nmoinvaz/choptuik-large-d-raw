@echo off
rem T41 diagnostic: D 3.40 at M 128 with the exact dd Jacobian, from the four clean M 128 states 3.5-3.425. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
set ST=%S%\t39-wt\hp\data\lowD_states
cd /d "%S%\t39-wt"
set PYTHONPATH=%S%\t39\pkg
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hp/lowD_dd.py hp/data/lowD_dd_local_t41_dd340.jsonl --start "%ST%\lowDvh41_D3.4250_M128.npz" --D 3.4 --history "%ST%\lowDvh_D3.5000_M128.npz,%ST%\lowDvh41_D3.4750_M128.npz,%ST%\lowDvh41_D3.4500_M128.npz" --Ms 128 --nodes 0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8 --kcs 100 --ks 250 --tol_step 1e-30 --it_max 30 --threads 1 --resume --tag lowDvh41dd --jac dd > "%S%\t41\dd340.log" 2>&1
echo exit %ERRORLEVEL% >> "%S%\t41\dd340.exit"
