@echo off
rem #1104 winb: the kappa 0.5 chain of my k_c 143 D 23.0 state (t5's order of 2026-11-27 18:23 UTC): the re-solve driver (source checks, ell_refine.py --kappa 0.5, acceptance); only if regrid_accepted.txt exists, the scan driver (d18_secant.py scan with the Rust block, 2 processes).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\k050d23_1104
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\k050d23_1104\k050d23_regrid_driver_1104.py > C:\Users\nathan\Source\k050d23_1104\k050d23_regrid_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\k050d23_1104\I1104-win\regrid_accepted.txt exit /b 1
if not exist C:\Users\nathan\Source\k050d23_1104\k050d23_scan_driver_1104.py exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\k050d23_1104\k050d23_scan_driver_1104.py "0.095,0.080;0.110,0.125" > C:\Users\nathan\Source\k050d23_1104\k050d23_scan_driver_stdout.log 2>&1
