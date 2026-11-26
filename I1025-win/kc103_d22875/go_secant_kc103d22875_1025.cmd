@echo off
rem #1025 winb: the secant refinement of the k_c 103 root at D 22.875 (t5's order of 2026-11-25 ~22:50 UTC, go-ahead 2026-11-26 ~03:47 UTC): one driver, bracket (0.100, 0.120) from the scan's reader.
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). The driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc103d22875_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc103d22875_1025\kc103d22875_secant_driver_1025.py 0.100 0.120 > C:\Users\nathan\Source\kc103d22875_1025\kc103d22875_secant_driver_stdout.log 2>&1
