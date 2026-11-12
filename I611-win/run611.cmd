@echo off
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I611-win
C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_611.py > logs\run_611.stdout 2>&1
echo %errorlevel% > logs\run_611.exit
