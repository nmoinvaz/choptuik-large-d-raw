@echo off
rem #951 (win): starts run_951_solves.py at BelowNormal; its children (the two rt_run.py solves) are started with BelowNormal too.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I951-win
start "solve951" /belownormal /wait /min C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_951_solves.py
