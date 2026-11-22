@echo off
rem #1025 winb (successor), the k_c 79 check part 1: the regrid driver (kc79_regrid_driver_1025.py), BelowNormal, detached. No GIT_CONFIG override: the worktree is CRLF and its pins use git diff and filtered hashes
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\kc79_1025
start "kc79regrid" /belownormal /wait /min C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\kc79_1025\kc79_regrid_driver_1025.py > C:\Users\nathan\Source\kc79_1025\kc79_regrid_driver_stdout.log 2>&1
