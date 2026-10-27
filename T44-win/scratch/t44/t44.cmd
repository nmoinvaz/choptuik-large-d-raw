@echo off
rem T44: sigma_15 pilot (2 x 3 processes), gate, then wf 0.99 and 1.01. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t44\t44_run.py" "%S%\t44-wt" > "%S%\t44\t44.out" 2>&1
