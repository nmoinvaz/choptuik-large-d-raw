@echo off
rem #1025 winb: P4 share (4 rows), third launch: the driver's git hash-object must hash raw bytes (two input blobs have CRLF; Git for Windows' system core.autocrlf=true changed their hashes), so the GIT_CONFIG_GLOBAL and GIT_CONFIG_SYSTEM environment variables point at /dev/null inside the shell. xtrace in driver_trace2.log. BelowNormal
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
set "THREADS=4"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\p4_1025
start "p4w" /belownormal /wait /min "C:\Program Files\Git\usr\bin\bash.exe" -c "export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null; bash -x /c/Users/nathan/Source/p4_1025/I1025-win/p4/p4_driver_w.sh C:/Users/nathan/Source/choptuik-i1025-lowd C:/Users/nathan/Source/p4_1025/raw C:/Users/nathan/Source/p4_1025/I1025-win/p4 > /c/Users/nathan/Source/p4_1025/driver_trace2.log 2>&1"
