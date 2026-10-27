@echo off
rem T41: the M 128 chain with the deflated Newton (--solver dn --jac dd). Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t41\t41c_chain.py" "%S%\t35-wt" "%S%\t39-wt" > "%S%\t41\t41c.out" 2>&1
