@echo off
rem #1025 winb, k_c 55 test: the alert-only memory watcher and the finisher for the running scan (pid 17520). Both BelowNormal, detached; neither touches the scan (the finisher only applies the order's 8 h time cap by exact pid)
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc55_1025
start "kc55watch" /belownormal /min C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc55_1025\kc55_watch_alert_1025.py 17520
start "kc55finish" /belownormal /min C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc55_1025\kc55_finish_1025.py 17520
