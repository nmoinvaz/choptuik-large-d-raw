@echo off
rem #1025 winb: the low-lambda scans on D 18.0625 and D 18 (scanlow_driver_1025.py): xfkappa's (ii), two processes. BelowNormal. GIT_CONFIG_* to /dev/null so git hash-object hashes the bytes as stored (core.autocrlf)
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "GIT_CONFIG_GLOBAL=/dev/null"
set "GIT_CONFIG_SYSTEM=/dev/null"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\scanlow_1025
start "scanlow" /belownormal /wait /min C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\scanlow_1025\scanlow_driver_1025.py > C:\Users\nathan\Source\scanlow_1025\scanlow_driver_stdout.log 2>&1
