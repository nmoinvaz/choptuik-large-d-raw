@echo off
rem T43 pilot (cloud 11:27): base and node06 from D 60.0020, 8 points, 0.75 h, 3 threads x 2 runs. Below-normal priority.
set S=C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad
set PY=C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe
cd /d "%S%\t43-wt\hp"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"%PY%" -u step_test.py --outdir data/step_test/pilot --D 60.0020 --variants base,node06 --max_points 8 --max_hours 0.75 --threads 3 --parallel 2 > "%S%\t43\pilot.out" 2>&1
set RC=%ERRORLEVEL%
"%PY%" step_test.py --report --outdir data/step_test/pilot > "%S%\t43\pilot_report.txt" 2>&1
set RR=%ERRORLEVEL%
"%PY%" step_test.py --report --outdir data/step_test/pilot --mutate=ref > "%S%\t43\pilot_report_mut.txt" 2>&1
set RM=%ERRORLEVEL%
echo run %RC% report %RR% mutated %RM% > "%S%\t43\pilot.exit"
