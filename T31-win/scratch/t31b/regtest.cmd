@echo off
rem T31b one-point test at D = 10.05 with --reg 1e-7, 1 thread. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
cd /d "%S%\t31-wt\solver\matter"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t31b\regtest.py" . "%S%\t31b\gate_kc31_D10.npy" "%S%\t31b\regtest_D10.05.npy" > "%S%\t31b\regtest.log" 2>&1
echo exit %ERRORLEVEL% >> "%S%\t31b\regtest.exit"
