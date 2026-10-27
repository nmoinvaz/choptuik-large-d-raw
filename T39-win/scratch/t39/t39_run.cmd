@echo off
rem T39: the T35 jobs not yet started, on lowD_dd.py --jac f64 (hpkernel d5bdb1a in t39\pkg). Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t39\t39_run.py" "%S%\t35-wt" "%S%\t39-wt" > "%S%\t39\t39_run.out" 2>&1
