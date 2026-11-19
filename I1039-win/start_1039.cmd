@echo off
rem #1039 (win): starts run_1039.py at BelowNormal; its children (the eight route3 runs, one at a time) are started at BelowNormal again.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I1039-win
start "run1039" /belownormal /wait /min C:\Users\nathan\Source\venv-choptuik-314\Scripts\python.exe -u run_1039.py
