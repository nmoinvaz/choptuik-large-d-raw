@echo off
rem #1104 winb: the kappa 0.5 secant refinement (t5's orders of 2026-11-28 08:37 and 08:39 UTC: the secant at tol 1e-5, maxev 12, 4 Rust threads, cap 28800 s in cap_seconds.txt, the scan's ends reused): one driver, the scan's bracket LO HI and the ends blob are the arguments below (written when the scan was read).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). The driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\k050d23_1104
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\k050d23_1104\k050d23_secant_driver_1104.py 0.095 0.11 --ends-blob=944e5150db498247dbba1e0e12cf9774859d41be > C:\Users\nathan\Source\k050d23_1104\k050d23_secant_driver_stdout.log 2>&1
