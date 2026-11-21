@echo off
rem #1025 winb follow-on: row B's dd sign check driver (ddB_driver_1025.py). It waits for "row B D 17.75: hybrid done" in p4hi_w.log, then runs ell_ddm.py det at root -/+ 0.02 (two processes, 4 threads each, 3 h cap each by exact pid). BelowNormal.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "GIT_CONFIG_GLOBAL=/dev/null"
set "GIT_CONFIG_SYSTEM=/dev/null"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\p4hi_1025
start "ddB" /belownormal /wait /min C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\p4hi_1025\ddB_driver_1025.py > C:\Users\nathan\Source\p4hi_1025\ddB_driver_stdout.log 2>&1
