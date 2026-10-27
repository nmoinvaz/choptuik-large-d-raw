@echo off
rem Starts T44 and T49 together once T45's leg has ended at D 3.05. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t44\t44_49_start.py" > "%S%\t44\t44_49_start.out" 2>&1
