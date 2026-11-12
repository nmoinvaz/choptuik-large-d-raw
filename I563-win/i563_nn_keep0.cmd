@echo off
cd /d C:\Users\nathan\Source\choptuik-i563\hp
set PATH=C:\Users\nathan\Source\venv-t151\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u %RAW%\I462-win\run_capped.py 7200 python.exe -u near_null.py %RAW% I461-win2/crawlJ/anm_pin3_D242.3642.npz --threads=2 --keep_plan=0 --json=%RAW%\I563-win\nn_keep0.json >%RAW%\I563-win\nn_keep0.log 2>&1
echo %errorlevel% > %RAW%\I563-win\nn_keep0.exit
