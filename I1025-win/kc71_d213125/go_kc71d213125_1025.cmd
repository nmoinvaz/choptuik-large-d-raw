@echo off
rem #1025 winb: lambda_1 at k_c 71 on leg 6's D 21.3125 state (t5's order of 2026-11-24 ~03:47 UTC): the scan driver with the ordered shares (4 processes, one per share; 8 evaluations: 0.785-0.815 by 0.005 and a repeat of 0.800).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff). The driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc71d213125_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc71d213125_1025\kc71d213125_scan_driver_1025.py "0.785,0.800;0.790,0.805;0.795,0.810;0.800,0.815" > C:\Users\nathan\Source\kc71d213125_1025\kc71d213125_scan_driver_stdout.log 2>&1
