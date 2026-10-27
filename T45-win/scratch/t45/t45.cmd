@echo off
rem T45 (cloud 18:53): waits for T43 to end, then step 0 (build, checks, M 384 pilot) and step 1. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t45\t45_run.py" "%S%\t45-wt" "%S%\t43" > "%S%\t45\t45.out" 2>&1
