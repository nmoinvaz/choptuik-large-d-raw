@echo off
cd /d C:\Users\nathan\Source\choptuik-t151\hp
set PATH=C:\Users\nathan\Source\venv-t151\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u %RAW%\I277-win\series_start.py %RAW% %RAW%\I277-win\d10_D214.5 --state I215-win/chain_d10/anm_pin3_D214.5000.npz --kfreeze 3 --held_fit data/held_fit_d10.json --N 24 --eps 1e-14 --h_max 0.5 --steps 1 --D_max 215 --threads 3 --corrector od --tol_od 1e-40 --qd_it 0 --jet_o 1 --reseed 2 --reseed_q 1 >> %RAW%\I277-win\d10_D214.5.log 2>&1
echo %errorlevel% > %RAW%\I277-win\d10_D214.5.exit
