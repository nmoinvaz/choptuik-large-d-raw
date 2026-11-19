@echo off
rem #1006 (win): starts run_1006.py at BelowNormal; its children (rt_xcount, the rt_sigma runs, one at a time) inherit the class and are started with it again.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I1006-win
start "run1006" /belownormal /wait /min C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_1006.py
