@echo off
cd /d C:\Users\nathan\Source\choptuik-i546\hp
set PATH=C:\Users\nathan\Source\venv-t151\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u %RAW%\I462-win\run_capped.py 14400 python.exe -u pole_bc.py %RAW%\I546-win\pole_bc_ks130.jsonl data/states/up8_D50.0075.npz data/states/up10_D55.0351.npz data/states/up13_D60.0020.npz --ks 130 --threads 1 > %RAW%\I546-win\pole_bc_ks130.log 2>&1
echo %errorlevel% > %RAW%\I546-win\pole_bc_ks130.exit
