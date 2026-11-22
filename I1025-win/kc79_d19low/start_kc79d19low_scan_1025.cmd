@echo off
rem #1025 winb, the k_c 79 lower-root scan at D 19, the scan driver (kc79d19low_scan_driver_1025.py), BelowNormal, detached (started through Win32_Process.Create), only when the coordinator has ordered it (the window is in the hc of 2026-11-22 ~17:35 UTC).
rem started as: conhost.exe --headless cmd.exe /c <this file> "<window>" (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff); the driver runs in this console (start /b)
rem usage: start_kc79d19low_scan_1025.cmd "0.92,0.96,1.00,1.04,1.08,1.12,1.16,1.20,1.24,1.28,1.32,1.12" [--dry]     (the window in quotes: a comma is a separator for cmd)
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc79d19low_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc79d19low_1025\kc79d19low_scan_driver_1025.py "%~1" %2 > C:\Users\nathan\Source\kc79d19low_1025\kc79d19low_scan_driver_stdout.log 2>&1
