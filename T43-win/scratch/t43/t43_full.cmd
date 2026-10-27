@echo off
rem T43 step 2 (cloud 11:27): all variants from the four D0, then --combo; 3 threads x 2 runs. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
set PY=C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe
cd /d "%S%\t43-wt\hp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"%PY%" -u step_test.py --combo --threads 3 --parallel 2 --max_points 20 --max_hours 1 --max_span 3 > "%S%\t43\full.out" 2>&1
set RC=%ERRORLEVEL%
"%PY%" step_test.py --report > "%S%\t43\full_report.txt" 2>&1
set RR=%ERRORLEVEL%
"%PY%" step_test.py --report --mutate=ref > "%S%\t43\full_report_mut.txt" 2>&1
set RM=%ERRORLEVEL%
echo run %RC% report %RR% mutated %RM% > "%S%\t43\full.exit"
