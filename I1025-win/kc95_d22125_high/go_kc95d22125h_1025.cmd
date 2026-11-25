@echo off
rem #1025 winb: the k_c 95 HIGH scan at D 22.125 chain (dh610's accepted k_c 95 state, not regridded) (t5's order of 2026-11-25 ~09:30 UTC): step 1, the source driver (pins, selftests, the source checks); step 2 only if source_accepted.txt exists, the scan driver with the ordered shares (8 evaluations, 4 processes).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc95d22125h_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc95d22125h_1025\kc95d22125h_source_driver_1025.py > C:\Users\nathan\Source\kc95d22125h_1025\kc95d22125h_source_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\kc95d22125h_1025\I1025-win\kc95_d22125_high\source_accepted.txt exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc95d22125h_1025\kc95d22125h_scan_driver_1025.py "0.60,0.52;0.64,0.56;0.68,0.72;0.64,0.76" > C:\Users\nathan\Source\kc95d22125h_1025\kc95d22125h_scan_driver_stdout.log 2>&1
