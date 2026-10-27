@echo off
rem T30 stage 1: lemma 6b_1 sweep pilot, 1 thread. Below-normal priority.
cd /d "C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t15-wt\solver\proof"
set OPENBLAS_NUM_THREADS=1
set OMP_NUM_THREADS=1
set PYTHONUNBUFFERED=1
"C:\Users\nathan\AppData\Local\Programs\Python\Python310\python.exe" -u lemma6_sweep.py --dfrac=0.001 --rhos=260,150,106.9,106.7,70,40,25 --out=t30_pilot.json > t30_pilot.log 2>&1
echo exit %ERRORLEVEL% >> t30_pilot.exit
