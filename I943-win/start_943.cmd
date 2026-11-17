@echo off
rem #943 (win): starts run_943.py at BelowNormal; its children (the two rt_sigma.py runs) inherit the class and are started with it again.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I943-win
start "run943" /belownormal /wait /min C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_943.py
