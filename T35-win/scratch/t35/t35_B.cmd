@echo off
rem T35 part B: M 128 / M 80 re-solves and gamma at D 3.6, 3.5, 3.4, 3.3 as their M 96 states land. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t35\t35_B.py" "%S%\t35-wt" > "%S%\t35\t35_B.out" 2>&1
