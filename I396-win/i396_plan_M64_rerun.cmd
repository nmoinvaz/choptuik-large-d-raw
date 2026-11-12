@echo off
cd /d C:\Users\nathan\Source\choptuik-i396b\hp
set PATH=C:\Users\nathan\Source\venv-t151\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u %RAW%\I462-win\run_capped.py 7200 python.exe -u plan_print.py data/states/up6_D30.0688.npz --M=64 --kf=none --threads=3 --json=%RAW%\I396-win\plan_win_M64_rerun.json >%RAW%\I396-win\plan_win_M64_rerun.log 2>&1
echo %errorlevel% > %RAW%\I396-win\plan_win_M64_rerun.exit
