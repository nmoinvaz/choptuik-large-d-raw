@echo off
rem #1025 winb: the lambda 1.20 dd check on D 18 and D 18.0625 (ref120_driver_1025.py), after the D 18.125 scan driver ends. BelowNormal. GIT_CONFIG_* to /dev/null so git hash-object hashes the bytes as stored (core.autocrlf)
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "GIT_CONFIG_GLOBAL=/dev/null"
set "GIT_CONFIG_SYSTEM=/dev/null"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\ref120_1025
start "ref120" /belownormal /wait /min C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\ref120_1025\ref120_driver_1025.py > C:\Users\nathan\Source\ref120_1025\ref120_driver_stdout.log 2>&1
