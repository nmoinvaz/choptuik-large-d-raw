@echo off
rem T37 lane %1: mode-count jobs from the queue, one at a time on one thread. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t37\t37_lane.py" "%S%\t37-wt" %1 > "%S%\t37\lane%1.out" 2>&1
