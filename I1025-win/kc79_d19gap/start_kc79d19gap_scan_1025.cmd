@echo off
rem #1025 winb, the k_c 79 gap scan (1.32, 1.475) at D 19, the scan driver (kc79d19gap_scan_driver_1025.py), BelowNormal, detached (started through Win32_Process.Create), only when the coordinator has ordered it (the window is in the hc of 2026-11-23 ~03:05 UTC).
rem started as: conhost.exe --headless cmd.exe /c <this file> "<window>" (Win32_Process.Create; win2's cim_start.ps1 form: no Windows Terminal handoff); the driver runs in this console (start /b)
rem usage: start_kc79d19gap_scan_1025.cmd "1.345,1.37,1.395,1.42,1.445,1.395" [--dry]     (the window in quotes: a comma is a separator for cmd)
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc79d19gap_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc79d19gap_1025\kc79d19gap_scan_driver_1025.py "%~1" %2 > C:\Users\nathan\Source\kc79d19gap_1025\kc79d19gap_scan_driver_stdout.log 2>&1
