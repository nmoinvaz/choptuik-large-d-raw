@echo off
rem #721 (win): starts run_721.py at BelowNormal; its child rt_sigma.py inherits the class.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I721-win
start "run721" /belownormal /wait /min C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_721.py
