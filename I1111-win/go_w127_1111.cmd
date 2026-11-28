@echo off
rem #1111 winb: R2 against chord035 on R2's map at k_c 127 D 23.0 (t5 hc 2026-11-28 10:58 UTC): jac, svd, detparts in one driver, BelowNormal, started by WMI (conhost.exe --headless cmd.exe /c this file).
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\k127d23_1111
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\k127d23_1111\w127_1111_driver.py > C:\Users\nathan\Source\k127d23_1111\driver_stdout_1111.log 2>&1
