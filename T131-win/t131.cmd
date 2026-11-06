@echo off
rem T131 (cloud 2026-11-06 08:23 UTC): quad-double second path over 162.8-175.6 in two segments in turn. Below normal, 4 threads, T125 build, main at 9855e119 reseed.py/anm_run.py.
cd /d C:\Users\nathan\Source\choptuik-t125\hp
set PATH=C:\Users\nathan\Source\venv-t125\Scripts;%PATH%
set RAW=..\..\choptuik-large-d-raw
python.exe -u anm_run.py %RAW% %RAW%\T131-win\chainA --state T127-win2/chain/anm_pin3_D162.8059.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.25 --steps 300 --D_max 169.9 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 >> %RAW%\T131-win\chainA.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t131\chainA.exit
python.exe -u anm_run.py %RAW% %RAW%\T131-win\chainB --state T127-win2/chain/anm_pin3_D170.2746.npz --kfreeze 3 --N 24 --eps 1e-14 --h_max 0.25 --steps 300 --D_max 175.6 --threads 4 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 >> %RAW%\T131-win\chainB.log 2>&1
echo %errorlevel% > C:\Users\nathan\AppData\Local\Temp\claude\C--Users-nathan-Source-dss-residual-kernel\86d2c1d2-48f9-41c1-9045-dff6a2020bf5\scratchpad\t131\chainB.exit
