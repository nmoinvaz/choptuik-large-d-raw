@echo off
rem #1025 winb: planted dd_logdet check in venv-md510, BelowNormal (started through start /belownormal)
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\md510-1025
start "ddchk" /belownormal /wait /min cmd.exe /c "C:\Users\nathan\Source\venv-md510\Scripts\python.exe -I check_dd_logdet_1025.py C:\Users\nathan\Source\md510-1025\check_dd_logdet_1025.json > C:\Users\nathan\Source\md510-1025\check_dd_logdet_1025.log 2>&1"
