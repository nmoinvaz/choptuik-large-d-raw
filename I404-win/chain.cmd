@echo off
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I404-win
C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u chain_404.py > logs\chain_404.stdout 2>&1
echo %errorlevel% > logs\chain_404.exit
