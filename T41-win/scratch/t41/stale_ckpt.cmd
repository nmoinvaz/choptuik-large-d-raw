@echo off
rem T41: keep failed checkpoints out of --resume's way. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u "%S%\t41\stale_ckpt.py" "%S%\t39-wt\hp\data\lowD_states" > "%S%\t41\stale_ckpt.log" 2>&1
