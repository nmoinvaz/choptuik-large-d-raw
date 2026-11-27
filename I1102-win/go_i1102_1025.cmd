@echo off
rem #1102 winb: the Windows gate of the Rust block 12 (t5's order of 2026-11-27 05:47 UTC): one driver, build into site/ then the four gates.
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). The driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\i1102_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\i1102_1025\gate_i1102_driver_1025.py > C:\Users\nathan\Source\i1102_1025\gate_i1102_driver_stdout.log 2>&1
