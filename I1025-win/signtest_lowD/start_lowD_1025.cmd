@echo off
rem #1025 winb: low-D signtests, 7 rows, detached at BelowNormal (the driver's own checks run first)
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PY=C:/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe"
set "ROWS_D=14.5,14,13.5,12,11.5,11,10.5"
set "BLAS_THREADS=4"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\signtest_lowD_1025
start "lowd" /belownormal /wait /min "C:\Program Files\Git\usr\bin\bash.exe" C:\Users\nathan\Source\signtest_lowD_1025\I1025-win\signtest_lowD\signtest_lowD_driver_v2.sh C:/Users/nathan/Source/choptuik-i1025-lowd C:/Users/nathan/Source/signtest_lowD_1025/raw C:/Users/nathan/Source/signtest_lowD_1025/I1025-win/signtest_lowD > C:\Users\nathan\Source\signtest_lowD_1025\driver_stdout.log 2>&1
