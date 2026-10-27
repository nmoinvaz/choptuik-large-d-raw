@echo off
rem T45 step 0 resumed (cloud 19:56): same-machine ref, scaled check, M 384 pilot, then step 1. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t45\t45_resume.py" "%S%\t45-wt" > "%S%\t45\t45_resume.out" 2>&1
