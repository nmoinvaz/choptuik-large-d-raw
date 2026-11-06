@echo off
rem T135 (cloud 2026-11-06 18:26 UTC): the low-D plan probe at M 384, 6 threads, below normal, T125 build, main at the checkout below (Python only past 266a4108).
cd /d C:\Users\nathan\Source\choptuik-t125\hp
set PATH=C:\Users\nathan\Source\venv-t125\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u lowD_plan_probe.py %RAW% %RAW%\T135-win\probe --state T105-win2/states/lowDhm_x0.000157-0.975_p1_D3.0438_M384.npz --targets 3.0425,3.043,3.0434 --N 3 --threads 6 --cap 900 > %RAW%\T135-win\probe.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t135\t135.exit
