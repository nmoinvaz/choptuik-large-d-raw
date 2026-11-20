@echo off
rem #1025 winb: P4 share (4 rows), second launch with the driver's stdout, stderr and xtrace in driver_trace.log (the first launch left nothing: its refusal text went to a console window); BelowNormal
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
set "THREADS=4"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\p4_1025
start "p4w" /belownormal /wait /min "C:\Program Files\Git\usr\bin\bash.exe" -c "bash -x /c/Users/nathan/Source/p4_1025/I1025-win/p4/p4_driver_w.sh C:/Users/nathan/Source/choptuik-i1025-lowd C:/Users/nathan/Source/p4_1025/raw C:/Users/nathan/Source/p4_1025/I1025-win/p4 > /c/Users/nathan/Source/p4_1025/driver_trace.log 2>&1"
