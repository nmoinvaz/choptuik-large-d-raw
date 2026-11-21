@echo off
rem #1025 winb: the D 18.125 hybrid sign scan in two processes (d18mid_driver_1025.py). BelowNormal. GIT_CONFIG_* to /dev/null so git hash-object hashes the bytes as stored (core.autocrlf)
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "GIT_CONFIG_GLOBAL=/dev/null"
set "GIT_CONFIG_SYSTEM=/dev/null"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\d18mid_1025
start "d18mid" /belownormal /wait /min C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\d18mid_1025\d18mid_driver_1025.py > C:\Users\nathan\Source\d18mid_1025\d18mid_driver_stdout.log 2>&1
