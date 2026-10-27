@echo off
rem T43 step 2 guard: stops the task if a base run fails its Delta check. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
set OPENBLAS_NUM_THREADS=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t43\t43_guard.py" "%S%\t43-wt\hp" > "%S%\t43\guard.out" 2>&1
