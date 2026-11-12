@echo off
cd /d C:\Users\nathan\Source\choptuik-large-d-raw\I611-win
C:\Users\nathan\Source\venv-t151\Scripts\python.exe -u run_611b.py kf13_D54c:kf13_D54a_D55.035148.npz:54.996085:13 kfm1_D54c:kfm1_D54a_D55.035148.npz:54.996085:-1 > logs\run_611b.stdout 2>&1
echo %errorlevel% > logs\run_611b.exit
