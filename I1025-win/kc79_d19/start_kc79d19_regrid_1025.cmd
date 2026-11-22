@echo off
rem #1025 winb, the k_c 79 check at D 19, the regrid driver (kc79d19_regrid_driver_1025.py), BelowNormal, detached (started through Win32_Process.Create). No GIT_CONFIG override: the worktree is CRLF and its pins use git diff and filtered hashes
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc79d19_1025
start "kc79d19regrid" /belownormal /wait /min C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc79d19_1025\kc79d19_regrid_driver_1025.py > C:\Users\nathan\Source\kc79d19_1025\kc79d19_regrid_driver_stdout.log 2>&1
