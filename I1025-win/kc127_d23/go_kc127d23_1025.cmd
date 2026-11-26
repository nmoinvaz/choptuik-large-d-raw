@echo off
rem #1025 winb: the k_c 127 D 23.0 chain (from macm3's k_c 119 state) (t5's order of 2026-11-26 ~10:40 UTC): step 1 and 2 and 3, the regrid driver (source checks, regrid, acceptance); step 4a only if regrid_accepted.txt exists, the scan driver (d18_secant.py scan, 2 processes).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc127d23_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc127d23_1025\kc127d23_regrid_driver_1025.py > C:\Users\nathan\Source\kc127d23_1025\kc127d23_regrid_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\kc127d23_1025\I1025-win\kc127_d23\regrid_accepted.txt exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc127d23_1025\kc127d23_scan_driver_1025.py "0.04,0.03,0.06;0.05,0.04" > C:\Users\nathan\Source\kc127d23_1025\kc127d23_scan_driver_stdout.log 2>&1
