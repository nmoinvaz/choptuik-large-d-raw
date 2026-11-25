@echo off
rem #1025 winb: the k_c 103 D 21.75 chain (from dh610's k_c 95 state) (t5's order of 2026-11-25 ~04:30 UTC): step 1, the regrid driver; step 2 only if regrid_accepted.txt exists, the scan driver with the ordered shares (6 evaluations, 4 processes).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc103d2175_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc103d2175_1025\kc103d2175_regrid_driver_1025.py > C:\Users\nathan\Source\kc103d2175_1025\kc103d2175_regrid_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\kc103d2175_1025\I1025-win\kc103_d2175\regrid_accepted.txt exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc103d2175_1025\kc103d2175_scan_driver_1025.py "0.645,0.635;0.640;0.650,0.655;0.645" > C:\Users\nathan\Source\kc103d2175_1025\kc103d2175_scan_driver_stdout.log 2>&1
