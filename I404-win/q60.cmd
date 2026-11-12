@echo off
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I404-win
C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_queue_404.py D60.0020 --nproc 4 > logs\queue_D60.0020.stdout 2>&1
echo %errorlevel% > logs\queue_D60.0020.exit
