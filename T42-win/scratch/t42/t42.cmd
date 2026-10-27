@echo off
rem T42: Newton-variant benchmark on an otherwise idle machine, after T38 ends (cloud 07:31, the user's order).
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t42\t42_run.py" "%S%\t42-wt" "%S%\t38" > "%S%\t42\t42.out" 2>&1
