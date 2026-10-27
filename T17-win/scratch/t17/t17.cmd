@echo off
rem T17: double-double gamma for every hp state, 6 single-threaded processes, below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15-wt"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set MKL_NUM_THREADS=1
set RAYON_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u hp\gamma_batch.py hp\data\local\gamma_dd.jsonl --procs=6 --m48=20,30,40,50 > hp\data\local\gamma_dd.log 2>&1
echo exit %ERRORLEVEL% >> t17_batch.exit
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" hp\gamma_compare.py hp\data\local\gamma_dd.jsonl > hp\data\local\gamma_compare.txt 2>&1
echo exit %ERRORLEVEL% >> t17_compare.exit
