@echo off
rem #1025 winb follow-on (hybrid roots at D 17.5 and 17.75, k_c 63): the driver waits for P4's "p4_driver_w.sh done" in p4_w.log, then runs row A and row B one at a time. BelowNormal, 4 threads.
rem GIT_CONFIG_* to /dev/null so git hash-object hashes the bytes as stored (core.autocrlf); /usr/bin/bash so no WSL launcher is found; xtrace in driver_trace_p4hi.log
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PY=C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
set "THREADS=4"
set "ROW_TIMEOUT=21600"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\p4hi_1025
start "p4hi" /belownormal /wait /min "C:\Program Files\Git\usr\bin\bash.exe" -c "export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null; /usr/bin/bash -x /c/Users/nathan/Source/p4hi_1025/p4hi_driver_1025.sh C:/Users/nathan/Source/choptuik-i1025-lowd C:/Users/nathan/Source/p4hi_1025/raw C:/Users/nathan/Source/p4hi_1025/I1025-win/p4_highD /c/Users/nathan/Source/p4_1025/I1025-win/p4/p4_w.log > /c/Users/nathan/Source/p4hi_1025/driver_trace_p4hi.log 2>&1"
