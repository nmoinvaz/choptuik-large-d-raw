@echo off
rem T132 (cloud 2026-11-06 13:59 UTC): the low-D plan probe, 6 threads, below normal, T125 build, main 7f7e6702 (Python only past 266a4108).
cd /d C:\Users\nathan\Source\choptuik-t125\hp
set PATH=C:\Users\nathan\Source\venv-t125\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u lowD_plan_probe.py %RAW% %RAW%\T132-win\probe --state T106-win2/pilot_M320_p1_N4/anm_lowd_D3.043750_M320.npz --targets 3.0425,3.043,3.0434 --N 3 --threads 6 --cap 900 > %RAW%\T132-win\probe.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t132\t132.exit
