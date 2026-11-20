@echo off
rem #1025 winb: k_c 63 lambda at D 16.5 (coordinator's job), detached at BelowNormal
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PY=/c/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe"
set "LOGS=/c/Users/nathan/Source/choptuik-i1025/logs1025"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\choptuik-i1025
start "d165" /belownormal /wait /min "C:\Program Files\Git\usr\bin\bash.exe" run_D16.5_1025.sh
