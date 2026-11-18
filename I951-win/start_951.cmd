@echo off
rem #951 (win): starts run_951.py at BelowNormal; its children (the two rt_sigma.py runs) inherit the class and are started with it again. %1 = t0, the start of the solves (UTC).
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I951-win
start "run951" /belownormal /wait /min C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_951.py --t0 "2026-11-18 01:49:22"
