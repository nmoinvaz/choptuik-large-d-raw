@echo off
rem T140 chain (cloud 2026-11-07 06:20 UTC): the pilot's command with --steps 200 and the degree-6 held fit, 3 threads, below normal, T125 build. >> keeps the log across restarts.
cd /d C:\Users\nathan\Source\choptuik-t125\hp
set PATH=C:\Users\nathan\Source\venv-t125\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u anm_run.py %RAW% %RAW%\T140-win\chain_d6 --state T81/conv_pin5_D73.0000_D73.000000.npz --kfreeze 3 --held_fit data/held_fit_d6.json --N 24 --eps 1e-14 --h_max 1.0 --steps 200 --D_max 165 --threads 3 --corrector qd --tol_qd 1e-28 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1 >> %RAW%\T140-win\chain_d6.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t140\chain_d6.exit
