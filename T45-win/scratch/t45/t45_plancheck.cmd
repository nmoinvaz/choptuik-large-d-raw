@echo off
rem T45 plan check (cloud 08:52): after the M 256/320 pair at D 3.1, M 256 re-solved on its own plan. Below normal.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t45\t45_plancheck.py" "%S%\t45-wt" > "%S%\t45\t45_plancheck.out" 2>&1
