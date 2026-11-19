@echo off
rem #1029 (win): starts run_1029.py at BelowNormal; its children (the amp_flint_par.py runs, two at once) are started at BelowNormal and their spawned workers inherit the class.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I1029-win
start "run1029" /belownormal /wait /min C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_1029.py
