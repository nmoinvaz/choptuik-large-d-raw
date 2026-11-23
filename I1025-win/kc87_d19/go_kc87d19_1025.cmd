@echo off
rem #1025 winb: the k_c 87 D 19 chain (t5's order of 2026-11-23 05:10 UTC): step 1, the regrid driver; step 2 only if regrid_accepted.txt exists, the scan driver with the ordered window.
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc87d19_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc87d19_1025\kc87d19_regrid_driver_1025.py > C:\Users\nathan\Source\kc87d19_1025\kc87d19_regrid_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\kc87d19_1025\I1025-win\kc87_d19\regrid_accepted.txt exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc87d19_1025\kc87d19_scan_driver_1025.py "1.380,1.405,1.430,1.455,1.480,1.505,1.530,1.555,1.580,1.480" > C:\Users\nathan\Source\kc87d19_1025\kc87d19_scan_driver_stdout.log 2>&1
