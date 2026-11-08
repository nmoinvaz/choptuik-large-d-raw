@echo off
rem hp build for Python 3.14 (venv-t179) in the worktree choptuik-i179. LTO off and 16 codegen units as the T151 build,
rem one cargo job, idle priority. Launched detached. Writes build.log, build.exit, mem_build.csv.
set RAW=C:\Users\nathan\Source\choptuik-large-d-raw\I179-win
set VENV=C:\Users\nathan\Source\venv-t179
set VIRTUAL_ENV=%VENV%
set PATH=%VENV%\Scripts;C:\Users\nathan\.cargo\bin;C:\Program Files\Git\usr\bin;C:\Program Files\Git\bin;%PATH%
set CARGO_PROFILE_RELEASE_LTO=false
set CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16
set CARGO_BUILD_JOBS=1
cd /d C:\Users\nathan\Source\choptuik-i179\hp
echo started %date% %time% > %RAW%\build.started
if exist %RAW%\mem_stop.flag del %RAW%\mem_stop.flag
start "memlog" /low /b powershell -NoProfile -ExecutionPolicy Bypass -File %RAW%\memlog.ps1
python -m pip uninstall -y multidouble > %RAW%\build.log 2>&1
start "build" /low /wait /b bash build.sh >> %RAW%\build.log 2>&1
echo %errorlevel% > %RAW%\build.exit
echo done > %RAW%\mem_stop.flag
