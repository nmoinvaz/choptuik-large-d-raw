@echo off
rem T35 side run: M = 80 continuation below D = 3.7 with a cubic predictor per step. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t35\t35_hist.py" "%S%\t35-wt" > "%S%\t35\t35_hist.out" 2>&1
