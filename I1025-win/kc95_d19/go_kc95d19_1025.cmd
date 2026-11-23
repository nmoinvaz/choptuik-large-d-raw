@echo off
rem #1025 winb: the k_c 95 D 19 chain (t5's order of 2026-11-23 12:45 UTC): step 1, the regrid driver; step 2 only if regrid_accepted.txt exists, the scan driver with the ordered window (15 evaluations).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc95d19_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc95d19_1025\kc95d19_regrid_driver_1025.py > C:\Users\nathan\Source\kc95d19_1025\kc95d19_regrid_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\kc95d19_1025\I1025-win\kc95_d19\regrid_accepted.txt exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc95d19_1025\kc95d19_scan_driver_1025.py "1.395,1.400,1.405,1.410,1.415,1.420,1.425,1.430,1.435,1.530,1.535,1.540,1.545,1.550,1.415" > C:\Users\nathan\Source\kc95d19_1025\kc95d19_scan_driver_stdout.log 2>&1
