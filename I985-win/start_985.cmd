@echo off
rem #985 (win): starts run_985.py at BelowNormal; its children (rt_xcount, rt_perturb, the rt_sigma runs, one at a time) inherit the class and are started with it again.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I985-win
start "run985" /belownormal /wait /min C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_985.py
