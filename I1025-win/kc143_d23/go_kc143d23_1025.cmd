@echo off
rem #1025 winb: the k_c 143 D 23.0 chain (from win2's k_c 135 state) (t5's order of 2026-11-27 05:59 UTC): the regrid driver (source checks, regrid, acceptance); only if regrid_accepted.txt exists, the scan driver (d18_secant.py scan with the Rust block, 2 processes).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc143d23_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc143d23_1025\kc143d23_regrid_driver_1025.py > C:\Users\nathan\Source\kc143d23_1025\kc143d23_regrid_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\kc143d23_1025\I1025-win\kc143_d23\regrid_accepted.txt exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc143d23_1025\kc143d23_scan_driver_1025.py "0.055,0.050;0.060,0.055" > C:\Users\nathan\Source\kc143d23_1025\kc143d23_scan_driver_stdout.log 2>&1
