@echo off
rem #1025 winb: the k_c 87 D 22.875 secant lane (t5's order of 2026-11-26 ~08:59 UTC): one driver, the scan's bracket (0.12, 0.13).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). The driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc87d22875s_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc87d22875s_1025\kc87d22875s_secant_driver_1025.py 0.12 0.13 > C:\Users\nathan\Source\kc87d22875s_1025\kc87d22875s_secant_driver_stdout.log 2>&1
