@echo off
rem #1025 winb lane: solver/matter/ell_win1025.sh (4 processes x 2 BLAS threads, every python under a 12 h timeout), detached at BelowNormal
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754"
set "PY=/c/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe"
set "LOGS=/c/Users/nathan/Source/choptuik-i1025/logs1025"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\choptuik-i1025\solver\matter
start "ell1025" /belownormal /wait /min "C:\Program Files\Git\usr\bin\bash.exe" -c "bash ell_win1025.sh > ../../logs1025/main.log 2>&1"
