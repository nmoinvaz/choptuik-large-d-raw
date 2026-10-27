@echo off
rem T15 (c3): kc 63 re-solves at 4.0, 3.7938, 3.7 from the kc 47 states with a long LM (maxjac 60, stall 8). 2 threads.
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
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\resolve_lm.py" "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t21-wt\solver" scan_lowD3_kc63_lm.jsonl 4.0000 neB_kc47_rk2_D4.0000.npy 63 60 8 >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\c3.log" 2>&1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\resolve_lm.py" "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t21-wt\solver" scan_lowD3_kc63_lm.jsonl 3.7938 neB_kc47_rk2_D3.7938.npy 63 60 8 >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\c3.log" 2>&1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\resolve_lm.py" "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t21-wt\solver" scan_lowD3_kc63_lm.jsonl 3.7000 neB_kc47_rk2_D3.7000.npy 63 60 8 >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\c3.log" 2>&1
echo exit %ERRORLEVEL% >> "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15\c3.exit"
