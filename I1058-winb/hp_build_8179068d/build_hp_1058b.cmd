@echo off
rem #1058 winb: hp build at main 8179068d. MSVC's link.exe first on PATH (vcvars64), then Git's usr\bin LAST (its link.exe is GNU coreutils'). Low-memory recipe from the coordinator. BelowNormal inherited from the launcher.
call "C:\Program Files\Microsoft Visual Studio\18\Community\VC\Auxiliary\Build\vcvars64.bat" > C:\Users\nathan\Source\hp1058_winb\vcvars.log 2>&1
set "PATH=%PATH%;C:\Users\nathan\.cargo\bin;C:\Program Files\Git\cmd;C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin"
set "PIP_NO_CACHE_DIR=1"
set "CARGO_PROFILE_RELEASE_LTO=false"
set "CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\hp1058_winb
"C:\Users\nathan\AppData\Local\Programs\Python\Python314\python.exe" -u driver_hp_1058b.py > C:\Users\nathan\Source\hp1058_winb\driver_stdout_b.log 2>&1
