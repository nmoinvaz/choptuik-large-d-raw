@echo off
cd /d C:\Users\nathan\Source\choptuik-i513\hp
set PATH=C:\Users\nathan\Source\venv-t151\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u %RAW%\I462-win\run_capped.py 10800 python.exe -u octo_corrector.py planted %RAW% I13-win/chain_d6/anm_pin3_D192.0000.npz --threads 3 --out %RAW%\I468-win\planted > %RAW%\I468-win\planted.log 2>&1
echo %errorlevel% > %RAW%\I468-win\planted.exit
