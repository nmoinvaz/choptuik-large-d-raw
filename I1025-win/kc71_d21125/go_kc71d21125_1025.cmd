@echo off
rem #1025 winb: lambda_1 at k_c 71 on leg 6's D 21.125 state (t5's order of 2026-11-24 ~01:45 UTC): the scan driver with the ordered shares (4 processes, one per share; 8 evaluations: 0.855-0.885 by 0.005 and a repeat of 0.870).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff). The driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc71d21125_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc71d21125_1025\kc71d21125_scan_driver_1025.py "0.855,0.870;0.860,0.875;0.865,0.880;0.870,0.885" > C:\Users\nathan\Source\kc71d21125_1025\kc71d21125_scan_driver_stdout.log 2>&1
