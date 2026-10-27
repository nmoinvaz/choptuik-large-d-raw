@echo off
rem T35 part C: f64 kc 55 / 63 at D = 3.7 from the double-double state (notes/LOW_D.md section 7). Below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t35-wt"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u solver/lowD_f64.py solver/data/lowD_f64_local.jsonl --dd hp/data/lowD_states/lowDv_D3.7000_M80.npz --kcs 55,63 --rks 2 --Ks 90 --threads 1 --gamma > solver/data/lowD_f64_local.log 2>&1
echo exit %ERRORLEVEL% >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t35\C.exit"
