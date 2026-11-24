@echo off
rem #1025 winb: the k_c 103 D 21.125 cross-build chain (from dh170's k_c 95 state) (t5's order of 2026-11-24 ~22:19 UTC): step 1, the regrid driver; step 2 only if regrid_accepted.txt exists, the scan driver with the ordered shares (6 evaluations, 4 processes).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc103d21125x_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc103d21125x_1025\kc103d21125x_regrid_driver_1025.py > C:\Users\nathan\Source\kc103d21125x_1025\kc103d21125x_regrid_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\kc103d21125x_1025\I1025-win\kc103_d21125x\regrid_accepted.txt exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc103d21125x_1025\kc103d21125x_scan_driver_1025.py "0.885,0.875;0.880;0.890,0.895;0.885" > C:\Users\nathan\Source\kc103d21125x_1025\kc103d21125x_scan_driver_stdout.log 2>&1
