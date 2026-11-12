@echo off
cd /d C:\Users\nathan\Source\choptuik-i513\hp
set PATH=C:\Users\nathan\Source\venv-t151\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u %RAW%\I462-win\run_capped.py 3600 python.exe -u %RAW%\I468-win\check_base.py %RAW% I468-win/chain_d6/base_pin3_D192.0000.npz %RAW%\I468-win\polish_d6.log --threads 3 --held_exact 1 > %RAW%\I468-win\check_base_he1.log 2>&1
echo %errorlevel% > %RAW%\I468-win\check_base_he1.exit
python.exe -u %RAW%\I462-win\run_capped.py 3600 python.exe -u %RAW%\I468-win\check_base.py %RAW% I468-win/chain_d6/base_pin3_D192.0000.npz %RAW%\I468-win\polish_d6.log --threads 3 --held_exact 1 --mutate dd > %RAW%\I468-win\check_base_he1_ctrl_dd.log 2>&1
echo %errorlevel% > %RAW%\I468-win\check_base_he1_ctrl_dd.exit
python.exe -u %RAW%\I462-win\run_capped.py 3600 python.exe -u %RAW%\I468-win\check_base.py %RAW% I468-win/chain_d6/base_pin3_D192.0000.npz %RAW%\I468-win\polish_d6.log --threads 3 --held_exact 1 --mutate shift > %RAW%\I468-win\check_base_he1_ctrl_shift.log 2>&1
echo %errorlevel% > %RAW%\I468-win\check_base_he1_ctrl_shift.exit
python.exe -u %RAW%\I462-win\run_capped.py 3600 python.exe -u %RAW%\I468-win\check_base.py %RAW% I468-win/chain_d6/base_pin3_D192.0000.npz %RAW%\I468-win\polish_d6.log --threads 3 --held_exact 0 > %RAW%\I468-win\check_base_he0.log 2>&1
echo %errorlevel% > %RAW%\I468-win\check_base_he0.exit
python.exe -u %RAW%\I462-win\run_capped.py 3600 python.exe -u %RAW%\I468-win\check_base.py %RAW% I468-win/chain_d6/base_pin3_D192.0000.npz %RAW%\I468-win\polish_d6.log --threads 3 --held_exact 0 --mutate dd > %RAW%\I468-win\check_base_he0_ctrl_dd.log 2>&1
echo %errorlevel% > %RAW%\I468-win\check_base_he0_ctrl_dd.exit
