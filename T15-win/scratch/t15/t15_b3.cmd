@echo off
rem T15 (b3): kc 55 at 3.7 from the kc 47 state with a long LM (maxjac 60, stall 8), then the sweep from 4.0 / 3.7938 / 3.7
rem with NE_HMIN 0.005 and NE_WEAK_TOL 2e-12, then (d3) kc 55 RK x4. 2 threads, below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t21-wt\solver\data"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONUNBUFFERED=1
set NE_RK=2
set NE_STRONG_TOL=2e-8
set NE_THREADS=2
set NE_WEAK_TOL=2e-12
set NE_LAM_EXTRA=scan_ne6_lowD_kc47.jsonl
set NE_SEED_KC=47
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\resolve_lm.py" "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t21-wt\solver" scan_lowD3_kc55_b3.jsonl 3.7 neB_kc47_rk2_D3.7000.npy 55 60 8 > "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\b3r.log" 2>&1
echo exit %ERRORLEVEL% >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\b3r.exit"
set NE_SEED_KC=
set NE_SEED_MIN=3.7
set NE_HMIN=0.005
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u ..\scan_ne.py scan_lowD3_kc55_b3.jsonl 4.0 3.3 0.05 0.05 0.6 neB_kc55_rk2_D 55 > "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\b3.log" 2>&1
echo exit %ERRORLEVEL% >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\b3.exit"
set NE_RK=4
set NE_SEED_MIN=3.3
set NE_LAM_EXTRA=scan_lowD3_kc55_b3.jsonl
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u ..\scan_ne.py scan_lowD3_kc55_rk4.jsonl 3.5 3.3 0.05 0.05 0.6 neB_kc55_rk2_D 55 > "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\d3.log" 2>&1
echo exit %ERRORLEVEL% >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\d3.exit"
