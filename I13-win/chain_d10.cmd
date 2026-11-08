@echo off
cd /d C:\Users\nathan\Source\choptuik-t151\hp
set PATH=C:\Users\nathan\Source\venv-t151\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u anm_run.py %RAW% %RAW%\I13-win\chain_d10 --state I13-win/pilot_d10/anm_pin3_D167.0000.npz --kfreeze 3 --held_fit data/held_fit_d10.json --N 24 --eps 1e-14 --h_max 1.0 --steps 200 --D_max 215 --threads 3 --corrector qd --tol_qd 1e-28 --qd_it 12 --jet_o 1 --reseed 2 --reseed_q 1 --save_pred 1 >> %RAW%\I13-win\chain_d10.log 2>&1
echo %errorlevel% > C:/Users/nathan/AppData/Local/Temp/claude/C--Users-nathan-Source-dss-residual-kernel/86d2c1d2-48f9-41c1-9045-dff6a2020bf5/scratchpad/i13/chain_d10.exit
