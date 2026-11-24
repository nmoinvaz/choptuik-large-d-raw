@echo off
rem #1025 winb: lambda_1 at k_c 87 on dh370's leg state D 21.125 (t5's order of 2026-11-24 ~07:22 UTC): the scan driver with the ordered shares (4 processes, one per share; 8 evaluations).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff). The driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc87d21125_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc87d21125_1025\kc87_scan_driver_1025.py "0.865,0.875;0.870,0.885;0.875,0.890;0.880" > C:\Users\nathan\Source\kc87d21125_1025\kc87_scan_driver_stdout.log 2>&1
