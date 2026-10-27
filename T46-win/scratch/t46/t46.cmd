@echo off
rem T46 (cloud 02:05): D = 4 lifted from M 80 to 96, 128, 160, 192 on the T45 build. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t46\t46_run.py" "%S%\t45-wt\hp" "%S%\t45\pkg" > "%S%\t46\t46.out" 2>&1
