@echo off
rem #943 (win): starts a second run_943.py driver at BelowNormal that adopts the two running rt_sigma.py launcher processes of the first driver (pids from logs/run_943.log),
rem with K 7's cap at 28 h counted from the first driver's start. Nothing is restarted.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I943-win
start "run943a" /belownormal /wait /min C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_943.py --adopt K7_D40=15796,K0_D40=8472 --t0 "2026-11-17 08:35:56"
