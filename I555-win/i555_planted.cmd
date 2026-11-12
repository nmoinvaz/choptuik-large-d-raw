@echo off
cd /d C:\Users\nathan\Source\choptuik-i555\hp
set PATH=C:\Users\nathan\Source\venv-t151\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u %RAW%\I462-win\run_capped.py 7200 python.exe -u octo_corrector.py planted %RAW% T129-win2/chain/anm_pin3_D180.5246.npz --threads 3 --out %RAW%\I555-win\planted > %RAW%\I555-win\planted.log 2>&1
echo %errorlevel% > %RAW%\I555-win\planted.exit
