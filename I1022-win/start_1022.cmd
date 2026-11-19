@echo off
rem #1022 (win): starts run_1022.py at BelowNormal; its children (the six rt_sigma.py runs, one at a time) inherit the class and are started with it again.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I1022-win
start "run1022" /belownormal /wait /min C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_1022.py
