@echo off
cd /d C:\Users\nathan\Source\choptuik-i513\hp
set PATH=C:\Users\nathan\Source\venv-t151\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u %RAW%\I462-win\run_capped.py 10800 python.exe -u anm_run.py %RAW% %RAW%\I468-win\chain_d10 --state I13-win/chain_d10/anm_pin3_D191.5000.npz --kfreeze 3 --held_fit data/held_fit_d10.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --D_max 215 --threads 3 --corrector od --tol_od 1e-40 --qd_it 12 --jet_o 1 --reseed 2 --reseed_q 1 --save_pred 1 > %RAW%\I468-win\polish.log 2>&1
echo %errorlevel% > %RAW%\I468-win\polish.exit
