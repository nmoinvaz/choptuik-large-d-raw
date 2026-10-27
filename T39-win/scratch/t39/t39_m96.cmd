@echo off
rem T35 chain below D = 3.45 directly at M = 96 with --jac f64, plus part B at 3.4 and 3.3. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t39\t39_m96.py" "%S%\t35-wt" "%S%\t39-wt" > "%S%\t39\t39_m96.out" 2>&1
