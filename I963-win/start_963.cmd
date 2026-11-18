@echo off
rem #963 (win): starts run_963.py at BelowNormal; its children (the four rt_sigma.py runs, one at a time) inherit the class and are started with it again.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I963-win
start "run963" /belownormal /wait /min C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_963.py
