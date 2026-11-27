@echo off
rem #1025 winb: the k_c 143 D 23.0 secant refinement (t5, hc 2026-11-27 16:28 UTC: run the secant on the scan bracket at tol 5e-5 on the Rust block; label the root a kappa 0.7 root): one driver, the scan bracket (0.050, 0.055), the scan ends reused.
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). The driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc143d23_1025
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc143d23_1025\kc143d23_secant_driver_1025.py 0.050 0.055 --ends-blob=64f040dc1d16ff34adea0342dde1a6407c347930 > C:\Users\nathan\Source\kc143d23_1025\kc143d23_secant_driver_stdout.log 2>&1
