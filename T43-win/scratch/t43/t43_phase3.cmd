@echo off
rem T43 phase 3 switch: reruns step 2's command with main's ranking once phase 3 begins. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t43\t43_phase3.py" > "%S%\t43\phase3.out" 2>&1
