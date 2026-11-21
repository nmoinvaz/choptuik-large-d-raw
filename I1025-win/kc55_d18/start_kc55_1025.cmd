@echo off
rem #1025 winb: the k_c 55 test at D 18 (kc55_driver_1025.py), one scan process with a memory watchdog. BelowNormal. GIT_CONFIG_* to /dev/null so git hash-object hashes the bytes as stored (core.autocrlf)
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "GIT_CONFIG_GLOBAL=/dev/null"
set "GIT_CONFIG_SYSTEM=/dev/null"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc55_1025
start "kc55" /belownormal /wait /min C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc55_1025\kc55_driver_1025.py > C:\Users\nathan\Source\kc55_1025\kc55_driver_stdout.log 2>&1
