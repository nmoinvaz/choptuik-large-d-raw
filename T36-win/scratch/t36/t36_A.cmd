@echo off
rem T36 job A: M = 7 solves at xi1 = 0.14, --procs 2. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t36\t36_job.py" "%S%\t36-wt\solver\inner_stokes" 0.14 "%S%\t36\m7_outer_xi014.txt" > "%S%\t36\job_A.out" 2>&1
