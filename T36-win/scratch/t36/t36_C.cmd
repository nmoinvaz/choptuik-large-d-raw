@echo off
rem T36 job C: the M = 9 pilot at the M = 7 zero, --procs 2. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t36\t36_jobC.py" "%S%\t36-wt\solver\inner_stokes" > "%S%\t36\job_C.out" 2>&1
