@echo off
rem T45 diagnosis: highm_check ref hashes on this machine with the new (main 7bce589) build, to compare builds here.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
cd /d "%S%\t45-wt\hp"
set PYTHONPATH=%S%\t45\pkg
set OPENBLAS_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u highm_check.py ref --save="%S%\t45\diag\ref_new.json" > "%S%\t45\diag\ref_new.log" 2>&1
echo exit %ERRORLEVEL% > "%S%\t45\diag\ref_new.exit"
