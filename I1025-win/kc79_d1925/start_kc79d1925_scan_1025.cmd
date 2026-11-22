@echo off
rem #1025 winb, the k_c 79 check at D 19.25, the scan driver (kc79d1925_scan_driver_1025.py), BelowNormal, detached (started through Win32_Process.Create), only when the coordinator has given the window.
rem usage: start_kc79d1925_scan_1025.cmd "1.55,1.56,1.57,1.58" [--dry]     (the window in quotes: a comma is a separator for cmd)
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc79d1925_1025
start "kc79d1925scan" /belownormal /wait /min C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc79d1925_1025\kc79d1925_scan_driver_1025.py "%~1" %2 > C:\Users\nathan\Source\kc79d1925_1025\kc79d1925_scan_driver_stdout.log 2>&1
