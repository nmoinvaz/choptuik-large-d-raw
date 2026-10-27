@echo off
rem --helper_fallback test (cloud 2026-10-24 23:41 UTC): a short low-M run where the M_c helper is forced to fail.
rem From the D 3.7 M 80/96 states: --diff_max 1e-30 moves up to 96/128 at 3.69 (so M_c = 80), --helper_it_max 1 makes
rem the M 80 helper fail at 3.68, and --helper_fallback must still converge M 96 there and record the pair. 6 threads.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
cd /d "%S%\t45-wt\hp"
set PYTHONPATH=%S%\t45\pkg
set OPENBLAS_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u lowD_highM.py --start_w data/lowD_states/highm15_D3.7000_M80.npz --start_n data/lowD_states/highm15_D3.7000_M96.npz --Ms 80,96,128 --dD 0.01 --D_end 3.665 --diff_max 1e-30 --tag fbtest --out data/lowD_highM/fallback_test.jsonl --points data/lowD_highM/fallback_test_points.jsonl --hours 2 --point_hours 2 --threads 6 --helper_fallback --helper_it_max 1 > "%S%\t45\fallback\fallback_test.log" 2>&1
echo exit %ERRORLEVEL% > "%S%\t45\fallback\fallback_test.exit"
